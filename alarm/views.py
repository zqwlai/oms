#coding: UTF-8 -*-

from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import time
import json
from django.utils.decorators import classonlymethod
from django.views.generic.base import View
from django.conf.urls import include, url
from oms.views import BaseResView
from common.alarm import send_mail
from common.decorators import  login_exempt
from common.falcon import  Falcon
from alarm.models import TMailServer

class EventcaseView(BaseResView):
    def get(self, request):
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 3600  # 默认取1个小时
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        return render(request, 'alarm/eventcase.html', locals())

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        fhostname = request.GET['fhostname']
        start_time = request.GET['start_time']
        end_time = request.GET['end_time']
        #将日期时间转换为时间戳
        start_timestamp = ''
        end_timestamp = ''
        if start_time:
            start_timestamp = int(time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S')))
        if end_time:
            end_timestamp = int(time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')))
        f = Falcon()
        #end_time = int(time.time())  # 必须要整形
        #start_time = end_time - 5 * 86400  # 30分钟
        data = f.get_eventcase(startTime=start_timestamp, endTime=end_timestamp, metrics='df.bytes.free.percent/fstype=', endpoints=fhostname)
        print data
        data = data[
               (page - 1) * limit: page * limit]
        print data
        return  HttpResponse(json.dumps({'total':len(data), 'rows':data}))

    def detail(self, request):
        id = request.GET['id']
        return render(request, 'alarm/eventcase_detail.html', locals())


    def queryevent(self, request):
        id = request.GET['id']
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        f = Falcon()
        data = f.get_events(event_id=id)
        total = len(data)
        data = data[
               (page - 1) * limit: page * limit]
        print data
        return HttpResponse(json.dumps({'total': total, 'rows': data}))

class SenderView(BaseResView):
    @login_exempt
    def mail(self, request):
        print request.POST.dict()
        tos = request.POST['tos']
        subject = request.POST['subject']
        content = request.POST['content']
        #获取邮件服务器信息
        mailserver_obj = TMailServer.objects.first()
        if not mailserver_obj:
            return JsonResponse({'code':1, 'message':'邮箱服务器未设置', 'data':''})
        mail_host = mailserver_obj.fhost
        mail_user = mailserver_obj.fuser
        mail_pass = mailserver_obj.fpassword
        send_mail(mail_host,mail_user,mail_pass, tos, subject, content)
        return JsonResponse({'code':0, 'data':'', 'message':'发送成功'})





