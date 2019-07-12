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





def  sms(request):
    print request.POST.dict()
    return HttpResponse("11111")




def mail(request):
    print request.POST.dict()
    return HttpResponse("11111")