proxy='127.0.0.1:8087'
proxies = {
    'http':'http://'+proxy,
    'https':'https://'+proxy,
}
path_wk = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  

firefox_proxy = '127.0.0.1'
firefox_port = '8087'
firefox_executable_path = 'C:\\tools\\geckodriver\\mozilla\\geckodriver'

save_folder = './download'
muti_pdf_dir = './download/muti_pdf_dir'

cn_nytimes_main_url = 'https://cn.nytimes.com/async/mostviewed/all/?lang=zh-hans'
cn_bbc_head_url = 'https://www.bbc.com'
cn_bbc_main_url = 'https://www.bbc.com/zhongwen/simp'
