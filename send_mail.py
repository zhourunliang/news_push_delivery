from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
import smtplib

import mail_config


def send_kindle(file_path, file_name):
    from_addr = mail_config.from_addr
    password = mail_config.password
    to_addr =  mail_config.to_addr
    smtp_server = mail_config.smtp_server

    # 邮件对象:
    msg = MIMEMultipart()
    msg['From'] = Header('新闻推送', 'utf-8').encode()
    msg['To'] = Header('kindle', 'utf-8').encode()
    msg['Subject'] = Header('convert', 'utf-8').encode()

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

def main():
    send_kindle('./pdf_out/test.pdf', 'test.pdf')

if __name__ == '__main__':
    main()