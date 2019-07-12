# -*- coding:utf-8 -*-

import sys
import json
import smtplib
import email.MIMEBase
import email.Encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
reload(sys) # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

def send_mail(msg,toaddrs,subject):
    '''''
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    @password:发信人的邮箱密码
    '''
    fromaddr = "zqwlai@126.com"
    smtpaddr = "smtp.126.com"
    password = "19870207aaa"

    mail_msg = MIMEMultipart()
    if not isinstance(subject,unicode):
        subject = unicode(subject, 'utf-8')
    mail_msg['Subject'] = subject
    mail_msg['From'] = '堡垒机系统'
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))
    ret = {'code':0, 'error':'', 'message':''}
    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr)  #连接smtp服务器
        s.starttls()
        s.login(fromaddr,password)  #登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string()) #发送邮件
        s.quit()
    except Exception,e:
       print "Error: unable to send email"
       print traceback.format_exc()
       ret['code'] = 1
       ret['error'] = str(e)
    return ret
