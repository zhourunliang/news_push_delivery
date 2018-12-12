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

cn_nytimes_main_url = 'https://cn.nytimes.com/async/mostviewed/all/?lang=zh-hans'
cn_bbc_head_url = 'https://www.bbc.com'
cn_bbc_main_url = 'https://www.bbc.com/zhongwen/simp'
