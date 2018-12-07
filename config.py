proxy='127.0.0.1:8087'
proxies = {
    'http':'http://'+proxy,
    'https':'https://'+proxy,
}
path_wk = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  
save_folder = './download'
img_save_folder = './download/img/'
pdf_out_folder = './pdf_out'
pdf_merger = './pdf_merger'
en_nytimes_head_link = 'https://www.nytimes.com'
cn_main_url = 'https://cn.nytimes.com/async/mostviewed/all/?lang=zh-hans'
