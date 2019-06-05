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
import traceback
import logging
logger_500 = logging.getLogger("500")
import sys
reload(sys)
sys.setdefaultencoding('utf8')



def index(request):
    return HttpResponseRedirect('/dashboard')

def dashboard(request):
    return render(request, 'dashboard.html',{'root_node':'dashboard'})

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
    print 555555
    logger_500.error('%s %s'%(request.request_id, traceback.format_exc()))

    if request.is_ajax() or request.method == 'POST':
        error_message = traceback.sys.exc_value.message
        if isinstance(error_message, tuple):
            result = {'code':error_message[0], 'message':error_message[1] ,'data':''}
        else:
            result = {'code':5000, 'data':'', 'message':traceback.format_exc()}
        return JsonResponse(result)
    return render(request, '500.html')

