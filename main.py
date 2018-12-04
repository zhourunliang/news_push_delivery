import requests
from pyquery import PyQuery as pq
import json
import os
import re
import pdfkit

import config
from model import News

def get_page(url):
    '''
    获取页面
    '''
    proxies = config.proxies
    try:
        res = requests.get(url,proxies=proxies, verify=False)
        # print(res.text)
    except requests.exceptions.ConnectionError as e:
        print('Error',e.args)
    page = res.content
    return page

def parse_page(page):
    e = pq(page)
    data = {}
    data['title'] = e('title').text()
    data['content'] = e('.article-content').html()
    data['imgs'] = [e(i).attr('src') for i in  e('.article-content img')]
    # print(data['imgs'])
    return data

def save_page(title, content):
    folder = config.save_folder
    filename = '{}.html'.format(title)
    path = os.path.join(folder, filename)
    with open(path, 'wb') as f:
        f.write(content.encode("utf-8"))
    return path

def get_news(url):
    page = get_page(url)
    data = parse_page(page)
    path = save_page(data['title'], data['content'])
    down_imgs(data['imgs'])
    return path, data['title']

def down_imgs(imgs):
    # print(imgs)
    folder = config.img_save_folder
    proxies = config.proxies
    for img in imgs:
        filename = img.split('/')[-1]
        # print(filename)
        path = os.path.join(folder, filename)
        r = requests.get(img, proxies=proxies, stream=True, verify=False)
        with open(path, 'wb') as f:
            f.write(r.content)

def html_deal(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        r = replace_img_url(s)
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(r)


def replace_img_url(content):
    # 将图片的绝对路径改为相对路径
    regex = re.compile(r'(\ssrc)\=[\"|\']http[s]?://[^\s]*/([^\s]*\.[\w]*)[\"|\']')
    r = regex.sub(r'\1="img/\2"', content)
    # print(r)
    return r

def save_pdf(path, title):
    #这样就不需要添加环境变量了
    path_wk = config.path_wk  
    #wkhtmltopdf包 安装位置
    configuration = pdfkit.configuration(wkhtmltopdf=path_wk)
    options = {
            'page-size': 'Letter',
            'minimum-font-size': 30,
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header' : [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'no-outline': None
    }
    out_path = os.path.join(config.pdf_out_folder, '{}.pdf'.format(title))
    pdfkit.from_file(path, out_path, configuration=configuration, options=options)

def single_page(url): 
    get_news_data = get_news(url)
    path = get_news_data[0]
    title = get_news_data[1]
    html_deal(path)
    save_pdf(path, title)

def main():
    # main_url = 'https://cn.nytimes.com/async/mostviewed/all/?lang=zh-hans'
    # page = get_page(main_url)
    # news_list = json.loads(page)
    # daily = news_list['list']['daily']
    # print(daily)
    single_page('https://cn.nytimes.com/world/20181203/trump-xi-g20-merkel/')

    

if __name__ == '__main__':
    main()