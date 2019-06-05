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
        print '111111'
        if not request.path.startswith('/static') and not request.path.startswith('/favicon.ico') and not request.path.startswith('/skin_config'):
            request.request_id = uuid.uuid1().get_hex()
            logger_request.info('%s %s'%(request.request_id, handler_paramer(request)))


    def process_response(self, request, response):
        print '222222'
        if not request.path.startswith('/static')  and not request.path.startswith('/favicon.ico') and  not request.path.startswith('/skin_config'):
            if request.is_ajax() or request.method == 'POST':
                try:
                    print 333333
                    logger_response.info('%s %s'%(request.request_id, response.content))
                    print 4444444
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
