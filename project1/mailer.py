#coding=utf-8

#Author: Jiangtian
#Create Date:2018/07/30
#Last Edited:2018/07/30

#简单的邮件发送模块。发送提醒邮件至特定的邮箱

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib

def send_email(to_addr, title, content):
    # Email地址和口令:
    from_addr = '3309095738@qq.com'
    password = 'omoamdjqeimidbfj'
    # SMTP服务器地址:
    smtp_server = 'smtp.qq.com'

    # 邮件对象:
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(title, 'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server, 465) # 25端口被阿里云封锁，使用465端口作为发送端口
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    print("sent email to {}".format(to_addr))
    server.quit()   

def send_image(to_addr, title, content):
    # Email地址和口令:
    from_addr = '3309095738@qq.com'
    password = 'omoamdjqeimidbfj'
    # SMTP服务器地址:
    smtp_server = 'smtp.qq.com'

    # 邮件对象:
    msg = MIMEMultipart()
    msg['Subject'] = Header(title, 'utf-8').encode()

    # 邮件正文是MIMEText:
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open('captcha.png', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'png', filename='test.png')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='test.png')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    server = smtplib.SMTP_SSL(smtp_server, 465) # 阿里云封锁了25端口，使用SSL加密后的465端口发送邮件
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    print("sent email to {}".format(to_addr))
    server.quit()
