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
                urls.append(url(r'^%s/%s' %
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

    for i in Service.objects.values('fcluster').distinct():
        fcluster = i['fcluster']
        success_num = Service.objects.filter(fcluster=fcluster, fstatus=1).count()
        unknow_num = Service.objects.filter(fcluster=fcluster, fstatus=0).count()
        fail_num = Service.objects.filter(fcluster=fcluster, fstatus=2).count()
        status_info.append({'fcluster':fcluster, 'data':[success_num,unknow_num, fail_num]})
    status_json = json.dumps(status_info)

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
    #判断用户是否存在
    if OmsUser.objects.filter(username=username):
        return JsonResponse({'code':1, 'data':'', 'message':'用户已经存在!'})

    #创建用户并跳转到dashboard
    OmsUser.objects.create_user(username=username,password=password, last_login=time.strftime('%Y-%m-%d %H:%M:%S'))
    user = auth.authenticate(username=username, password=password)
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

