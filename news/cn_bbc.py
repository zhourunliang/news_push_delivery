import requests
from pyquery import PyQuery as pq
import json
import os
import re
import pdfkit
from PyPDF2 import PdfFileMerger
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import config
from news import News
from utils import *


options = Options()
options.add_argument('-headless')

profile = FirefoxProfile()
# 激活手动代理配置（对应着在 profile（配置文件）中设置首选项）
profile.set_preference("network.proxy.type", 1)
# ip及其端口号配置为 http 协议代理
profile.set_preference("network.proxy.http", config.firefox_proxy)
profile.set_preference("network.proxy.http_port", config.firefox_port)

profile.set_preference("network.proxy.ssl", config.firefox_proxy)
profile.set_preference("network.proxy.ssl_port", config.firefox_port)

# 所有协议共用一种 ip 及端口，如果单独配置，不必设置该项，因为其默认为 False
# profile.set_preference("network.proxy.share_proxy_settings", True)

# 默认本地地址（localhost）不使用代理，如果有些域名在访问时不想使用代理可以使用类似下面的参数设置
# profile.set_preference("network.proxy.no_proxies_on", "localhost")
profile.update_preferences()
driver = webdriver.Firefox(executable_path=config.firefox_executable_path, firefox_profile=profile, firefox_options=options)

# driver.close()

class CnBBC(News):
    def __init__(self):
        date = time.strftime("%Y-%m-%d")
        self.html_dir = config.save_folder+'/cn_bbc/'+date+'/html'
        self.img_dir = config.save_folder+'/cn_bbc/'+date+'/html/img'
        self.single_pdf_dir = config.save_folder+'/cn_bbc/'+date+'/single_pdf_dir'
        self.muti_pdf_dir = config.save_folder+'/muti_pdf_dir'
        make_dirs(self.html_dir)
        make_dirs(self.img_dir)
        make_dirs(self.single_pdf_dir)
        make_dirs(self.muti_pdf_dir)

    @classmethod
    def _parse_page(cls, page):
        e = pq(page)
        data = {}
        data['title'] = e('title').text()
        data['content'] = e('.story-body').remove('.with-extracted-share-icons').html()
        data['imgs'] = [e(i).attr('src') for i in  e('.story-body img')]
        # print(data['imgs'])
        return data

    @classmethod
    def _single_page(cls, url): 
        print('getting url ...', url)
        page = get_html(url)
        data = cls._parse_page(page)
        if data['content'] is None:
            return False
        title = data['title']
        content = replace_img_url(data['content'])

        html_path = os.path.join(cls().html_dir, title+'.html')
        # print('html_path', html_path)        
        save_html(html_path, content)
        down_imgs(data['imgs'], cls().img_dir)
        pdf_path = os.path.join(cls().single_pdf_dir, title+'.pdf')
        save_pdf(html_path, pdf_path)

    @classmethod
    def _parse_list(cls, page):
        e = pq(page)
        # print('')
        news_list = [config.cn_bbc_head_url + e(i).attr('href') for i in e('.most-popular__list-container a')]
        return news_list

    @classmethod
    def _get_most_popular(cls, url):
        driver.get(url)
        time.sleep(5)
        page = driver.page_source
        driver.close()
        # print(page)
        # save_html('bbc.html',page)
        news_list = cls._parse_list(page)
        return news_list

    def main(self):
        main_url = config.cn_bbc_main_url
        most_popular_news = self._get_most_popular(main_url)
        print('most_popular_news', most_popular_news)
        for url in most_popular_news:
            # print('item', item)
            self._single_page(url)

        pdfs = get_all_file(self.single_pdf_dir)
        filename = 'cn_bbc_{}.{}'.format(time.strftime("%Y-%m-%d"),'pdf')
        out_path = os.path.join(self.muti_pdf_dir, filename)    
        merger_pdf(pdfs, out_path)

        # self._single_page('https://www.bbc.com/zhongwen/simp/world-46533135')