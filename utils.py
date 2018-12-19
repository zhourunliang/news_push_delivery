import os
import re
import requests
import pdfkit
from PyPDF2 import PdfFileMerger

import config

def get_html(url):
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

def save_html(path, content):
    '''
    保存html
    '''
    with open(path, 'wb') as f:
        f.write(content.encode("utf-8"))
    return path

def replace_img_url(content):
    '''
    将图片的绝对路径改为相对路径
    '''
    regex = re.compile(r'(\ssrc)\=[\"|\']http[s]?://[^\s]*/([^\s]*\.[\w]*)[\"|\']')
    r = regex.sub(r'\1="img/\2"', content)
    # print(r)
    return r

def down_imgs(imgs, folder):
    '''
    下载图片
    '''
    # print(imgs)
    proxies = config.proxies
    for img in imgs:
        filename = img.split('/')[-1]
        # print(filename)
        path = os.path.join(folder, filename)
        r = requests.get(img, proxies=proxies, stream=True, verify=False)
        with open(path, 'wb') as f:
            f.write(r.content)


def get_all_file(path, fileList=[]):
    '''
    获取指定目录下所有的文件
    '''
    get_dir = os.listdir(path)  #遍历当前目录，获取文件列表
    for i in get_dir:
        sub_dir = os.path.join(path,i)  # 把第一步获取的文件加入路径
        # print(sub_dir)
        if os.path.isdir(sub_dir):     #如果当前仍然是文件夹，递归调用
            get_all_file(sub_dir, fileList)
        else:
            ax = os.path.abspath(sub_dir)  #如果当前路径不是文件夹，则把文件名放入列表
            # print(ax)
            fileList.append(ax)
    return fileList

def save_pdf(in_path, out_path):
    '''
    保存pdf文件
    '''
    #这样就不需要添加环境变量了
    path_wk = config.path_wk  
    #wkhtmltopdf包 安装位置
    configuration = pdfkit.configuration(wkhtmltopdf=path_wk)
    options = {
            'page-size': 'Letter',
            'minimum-font-size': 60,
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
    # out_path = os.path.join(config.pdf_out_folder, '{}.pdf'.format(title))
    pdfkit.from_file(in_path, out_path, configuration=configuration, options=options)


def merger_pdf(pdfs, out_path):
    '''
    合并多个pdf
    '''
    merger = PdfFileMerger()
    for pdf in pdfs:
       bookmark = os.path.basename(os.path.splitext(pdf)[0])
       merger.append(open(pdf, 'rb'), bookmark=bookmark)
 
    output = open(out_path, "wb")
    merger.write(output)


def make_dirs(file_dir):
    '''
    检查文件夹是否存在，没有则创建
    '''
    #判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)


