import requests
from pyquery import PyQuery as pq
import json
import os
import re
import pdfkit
from PyPDF2 import PdfFileMerger
import time

import config
from news import News
from utils import *

class CnNytimes(News):
    def __init__(self):
        date = time.strftime("%Y-%m-%d")
        self.html_dir = config.save_folder+'/cn_nytimes/'+date+'/html'
        self.img_dir = config.save_folder+'/cn_nytimes/'+date+'/html/img'
        self.single_pdf_dir = config.save_folder+'/cn_nytimes/'+date+'/single_pdf_dir'
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
        data['content'] = e('.article-content').html()
        data['imgs'] = [e(i).attr('src') for i in  e('.article-content img')]
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
        save_html(html_path, content)
        down_imgs(data['imgs'], cls().img_dir)
        pdf_path = os.path.join(cls().single_pdf_dir, title+'.pdf')
        save_pdf(html_path, pdf_path)

    @classmethod
    def _get_daily_news(cls, url):
        page = get_html(url)
        news_list = json.loads(page)
        daily = news_list['list']['daily']
        return daily

    def main(self):
        main_url = config.cn_nytimes_main_url
        daily = self._get_daily_news(main_url)
        for item in daily:
            # print('item', item)
            self._single_page(item['url'])

        pdfs = get_all_file(self.single_pdf_dir)
        filename = 'cn_nytimes_daily_{}.{}'.format(time.strftime("%Y-%m-%d"),'pdf')
        out_path = os.path.join(self.muti_pdf_dir, filename)    
        merger_pdf(pdfs, out_path)