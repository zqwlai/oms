#coding: UTF-8 -*-

from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from  user_app.models import OmsUser
import time
import json
from django.utils.decorators import classonlymethod
from django.views.generic.base import View
from django.conf.urls import include, url
from service_app.models import Service
from docker.models import VirtualMachine
from common.falcon import Falcon
from oms import  settings
import traceback
import logging
logger_500 = logging.getLogger("500")
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class BaseResView(View):

    @classonlymethod
    def urls(cls, **initkwargs):
        name = cls.__name__
        # 去掉类名中的view
        name = name.lower().replace('view', '')
        instance = cls(**initkwargs)
        urls = []
        urls.append(url(r'^%s$' % name, cls.as_view()))
        for k, v in cls.__dict__.iteritems():
            if not k.startswith('_'):
                urls.append(url(r'^%s/%s/$' %
                                (name, k), getattr(instance, k)))
                urls.append(url(r'^%s/%s$' %
                                (name, k), getattr(instance, k)))
        return urls


def index(request):
    return HttpResponseRedirect('/dashboard')

def dashboard(request):
    #统计集群数，服务数、机器数
    cluster_count = Service.objects.values('fcluster').distinct().count()
    service_count = Service.objects.values('fhost', 'fname', 'fport').distinct().count()
    host_count = Service.objects.values('fhost').distinct().count()

    #统计每个集群的健康度
    status_info = []

    cluster_list = []
    success_rate_list = []
    series = []
    success_num_list = []
    unknow_num_list = []
    fail_num_list = []
    for i in Service.objects.values('fcluster').distinct():
        fcluster = i['fcluster']
        cluster_list.append(fcluster)

        success_num = int(Service.objects.filter(fcluster=fcluster, fstatus=1).count())
        unknow_num = int(Service.objects.filter(fcluster=fcluster, fstatus=0).count())
        fail_num = int(Service.objects.filter(fcluster=fcluster, fstatus=2).count())
        total = success_num+unknow_num+fail_num


        success_num_list.append(success_num)
        unknow_num_list.append(unknow_num)
        fail_num_list.append(fail_num)
        if total == 0:
            success_rate = 100
        else:
            success_rate = '%.2f'%(float(success_num)/total*100)
            success_rate = float(success_rate)
        success_rate_list.append(success_rate)
        status_info.append({'fcluster':fcluster, 'success_num':success_num,'unknow_num':unknow_num,
                            'fail_num':fail_num, 'total_num':success_num+unknow_num+fail_num})
    series.append({'name':'正常服务数', 'data':success_num_list, 'color':'#008000'})
    series.append({'name': '未知服务数', 'data': unknow_num_list, 'color':'#FF8C00'})
    series.append({'name': '异常服务数', 'data': fail_num_list, 'color':'#FF0000'})
    series = json.dumps(series)
    status_json = json.dumps(status_info)
    #success_rate_list = json.dumps(success_rate_list)
    cluster_list = json.dumps(cluster_list)

    #统计最近10次的告警事件
    hostname_list = [i['fhostname'] for i in Service.objects.values('fhostname').distinct()]
    for i in VirtualMachine.objects.all():
        hostname_list.append(i.fmaster + '/' + i.fhostname)
    hostname_list = list(set(hostname_list))
    if not hostname_list:
        eventcase_list = []
    else:
        f = Falcon()
        eventcase_list = f.get_eventcase(endpoints=hostname_list)
        eventcase_list = eventcase_list[0:10]
    #print eventcase_list
    return render(request, 'dashboard.html',locals())

def process_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        # isadmin=is_admin(request.user)
        return HttpResponseRedirect('/dashboard')
    else:
        return render(request, 'login.html', {'err': '用户名或密码不正确！'})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register(request):
    return render(request, 'register.html')


def process_register(request):
    username = request.POST['username']
    password = request.POST['password']
    cname = request.POST['cname']
    email = request.POST['email']

    f = Falcon()
    ret = f.register(username, password, cname, email)
    if ret.has_key('error'):
        return JsonResponse({'code':1, 'data':'', 'message':ret['error']})

    user = auth.authenticate(username=username, password=password)
    print user
    auth.login(request, user)
    return JsonResponse({'code':0, 'data':'', 'message':'用户注册成功!'})



def handler_404(request):
    if request.is_ajax() or request.method == 'POST':
        result = {'code': 1,
            'data': '',
            'message':'您所请求的内容不存在'}
        return JsonResponse(result)
    else:
        return render(request, '404.html')



def handler_500(request):
    logger_500.error('%s %s'%(request.request_id, traceback.format_exc()))

    if request.is_ajax() or request.method == 'POST':
        error_message = traceback.sys.exc_value.message
        if isinstance(error_message, tuple):
            result = {'code':error_message[0], 'message':error_message[1] ,'data':''}
        else:
            result = {'code':5000, 'data':'', 'message':traceback.format_exc()}
        return JsonResponse(result)
    return render(request, '500.html')



def getcomponent(request):  #获取对应主机下所有的组件信息
    hostname = request.POST['hostname']
    Service.objects.filter(fhostname=hostname)
    data = []
    for i in Service.objects.filter(fhostname=hostname):
        data.append({'fname':i.fname, 'fport':i.fport,'fadmin_user':i.fadmin_user,'fadmin_password':i.fadmin_password})
    return JsonResponse({'code':0, 'data':data, 'message':'ok'})

def getContainer(request):
    data = {}
    for i in VirtualMachine.objects.all():
        if i.fmaster in data:
            data[i.fmaster].append(i.fhostname)
        else:
            data[i.fmaster] = [i.fhostname]
    return JsonResponse({'code': 0, 'data': data, 'message': 'ok'})


def addContainer(request):
    fhostname = request.POST['fhostname']
    fmaster = request.POST['fmaster']
    fip = request.POST.get('fip', '')
    if not VirtualMachine.objects.filter(fhostname=fhostname, fmaster=fmaster):
        VirtualMachine.objects.create(fhostname=fhostname, fmaster=fmaster, fip=fip)
    return JsonResponse({'code': 0, 'data': '', 'message': 'ok'})

