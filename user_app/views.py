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


def update_profile(request):
    user_id = int(request.POST['user_id'])
    arg_dict = request.POST.dict()
    #判断当前修改用户是否是自己
    if user_id != request.user.id:
        return JsonResponse({'code':1, 'data':'', 'message':'没有权限修改该用户信息！'})
    OmsUser.objects.filter(id=user_id).update(email=arg_dict['email'], phone=int(arg_dict['phone']))
    return JsonResponse({'code':0, 'data':'', 'message':'更新成功！'})


def update_password(request):
    try:
        user_id = int(request.POST['user_id'])
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        repeat_password = request.POST['repeat_password']
        #判断当前修改用户是否是自己
        if user_id != request.user.id:
            return JsonResponse({'code':1, 'data':'', 'message':'没有权限修改该用户信息！'})

        #再判断原密码是否是对的
        if not request.user.check_password(old_password):
            return JsonResponse({'code':1, 'data':'', 'message':'原密码不正确！'})

        request.user.set_password(new_password)
        request.user.save()
    except Exception, e:
        print e

    return JsonResponse({'code':0, 'data':'', 'message':'更新成功！'})