proxy='127.0.0.1:8087'
proxies = {
    'http':'http://'+proxy,
    'https':'https://'+proxy,
}
path_wk = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  
save_folder = './download'
img_save_folder = './download/img/'
pdf_out_folder = './pdf_out'