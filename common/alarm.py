#!-*- coding:utf8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def check_mailserver(mail_host, mail_user, mail_pass):
    ret = {'status':0, 'message':'ok'}
    print mail_host, mail_user, mail_pass
    try:
        smtpObj = smtplib.SMTP(timeout=5)
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
    except Exception,e:
        ret['status'] = 1
        ret['message'] = str(e)
    print ret
    return ret




def send_mail(mail_host, mail_user, mail_pass, tos, subject, content):
    sender = '%s@%s'%(mail_user, '.'.join(mail_host.split('.')[-2:]))
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = tos.split(',')

    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题
    message['Subject'] = subject
    #发送方信息
    message['From'] =  formataddr(['苍穹告警', sender])
    #接受方信息
    message['To'] = tos

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass)
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        #退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
        raise Exception('error', e)
