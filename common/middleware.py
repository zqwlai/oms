#coding: UTF-8 -*-
from common.utils import  get_md5sum, handler_paramer
import logging
logger_request = logging.getLogger("request")
logger_response = logging.getLogger("response")
logger_500 = logging.getLogger("500")
import uuid
import traceback
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
from django.contrib import auth
import urllib,urllib2
from django.http import JsonResponse

class LogRecordMiddleware(object):

    def process_request(self, request):
        if not request.path.startswith('/site_static') and not request.path.startswith('/favicon.ico') and not request.path.startswith('/skin_config'):
            request.request_id = uuid.uuid1().get_hex()
            logger_request.info('%s %s'%(request.request_id, handler_paramer(request)))


    def process_response(self, request, response):
        if not request.path.startswith('/site_static')  and not request.path.startswith('/favicon.ico') and  not request.path.startswith('/skin_config'):
            if request.is_ajax() or request.method == 'POST':
                try:
                    logger_response.info('%s %s'%(request.request_id, response.content))

                except:
                    logger_response.info('%s %s'%(request.request_id, response))
        return response



class LoginMiddleware(object):

    def process_view(self, request, view, args, kwargs):
        if getattr(view, 'login_exempt', False):
            return None

        if not request.user.is_authenticated():
            if request.is_ajax():
                return JsonResponse({'code':3, 'message':'login required'})
            return HttpResponseRedirect('/login')


class RbacMiddleware(object):
    """判断请求过来的url是否在所属菜单中."""

    def process_view(self, request, view, args, kwargs):
        if getattr(view, 'login_exempt', False):
            return None
        if request.user and request.user.is_superuser:
            return

        if request.path in ['/', 'login', '/user/profile', '/dashboard']:
            return
        acccept_url_list = []
        #查询此用户的角色
        role_list = request.user.tsysrole_set.all()
        for role_obj in role_list:
            for permission in role_obj.permissions.all():
                acccept_url_list.append(permission.fresource_url)
        acccept_url_list = list(set(acccept_url_list))

        accept = False
        for url in acccept_url_list:
            if request.path.find(url) == 0:
                accept = True
        if accept:
            return
        return HttpResponse(json.dumps({'code':403, 'message':'没有访问权限,请联系管理员配置新用户对应的默认角色','data':''},ensure_ascii=False))

