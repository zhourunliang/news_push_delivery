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
    __fields__ =  [
        ('news_list', dict, {}),
    ]

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
        html_path = os.path.join(config.save_folder, title+'.html')        
        save_html(html_path, content)
        down_imgs(data['imgs'], config.img_save_folder)
        pdf_path = os.path.join(config.pdf_out_folder, title+'.pdf')
        save_pdf(html_path, pdf_path)

    @classmethod
    def _get_daily_news(cls, url):
        page = get_html(url)
        news_list = json.loads(page)
        daily = news_list['list']['daily']
        return daily

    @classmethod
    def main(cls):
        cn_main_url = config.cn_main_url
        daily = cls._get_daily_news(cn_main_url)
        for item in daily:
            # print('item', item)
            cls._single_page(item['url'])

        pdfs = get_all_file(config.pdf_out_folder)
        filename = 'cn_nytimes_daily_{}.{}'.format(time.strftime("%Y-%m-%d"),'pdf')
        out_path = os.path.join(config.pdf_merger, filename)    
        merger_pdf(pdfs, out_path)