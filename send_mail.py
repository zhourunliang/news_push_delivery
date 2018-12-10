from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
import smtplib
import os

from utils import get_all_file
import config
import mail_config

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_kindle(file_path, file_name):
    from_addr = mail_config.from_addr
    password = mail_config.password
    to_addr =  mail_config.to_addr
    smtp_server = mail_config.smtp_server

    # 邮件对象:
    msg = MIMEMultipart()

    msg['From'] = _format_addr('新闻推送 <%s>' % from_addr)
    msg['To'] = _format_addr('kindle <%s>' % to_addr)
    msg['Subject'] = Header('kindle', 'utf-8').encode()

    # 邮件正文是MIMEText:
    msg.attach(MIMEText('convert', 'plain', 'utf-8'))

    # 构造附件，传送当前目录下的文件
    attr = MIMEApplication(open(file_path,'rb').read())
    attr.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(attr)

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def send_news_emil():
    file_list = get_all_file(config.pdf_merger)
    # print(file_list)
    for file in file_list:
        file_name = os.path.basename(file)
        send_kindle(file, file_name)


