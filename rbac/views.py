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
from rbac.models import TSysPermission
from oms import settings
import traceback


def menu_list(request):
    return render(request, 'rbac/menu_list.html',{'root_node':'rbac','child_node':'menu'})


def data(request):
    znode = [{'fid': 0, 'name': '导航菜单', 'open': 'true', 'children': []}]

    data = []
    for i in TSysPermission.objects.filter(fparent_id=0).order_by('flocal'):
        if not TSysPermission.objects.filter(fparent_id=i.fid):  # 判断该一级节点有没有子节点
            data.append({
                'fid': int(i.fid), 'name': i.fresource_name, 'open': 'true',
                'isParent': 'true', 'flocal': int(i.flocal), 'fenable': int(i.favailable),
                'ficon': str(i.fmenu_icon), 'fresource_url': str(i.fresource_url)
            })
        else:
            level2_data = []
            for j in TSysPermission.objects.filter(fparent_id=i.fid).order_by('flocal'):        #遍历子节点
                level2_data.append({
                    'fid': int(j.fid), 'name': j.fresource_name,
                    'flocal': int(j.flocal), 'fenable': int(j.favailable),
                    'ficon': str(j.fmenu_icon), 'fresource_url': str(j.fresource_url)
                })
            data.append({
                'fid': int(i.fid), 'name': i.fresource_name,
                'open': 'true', 'isParent': 'true', 'children': level2_data,
                'flocal': int(i.flocal), 'fenable': int(i.favailable),
                'ficon': str(i.fmenu_icon), 'fresource_url': str(i.fresource_url)
            })
    znode[0]['children'] = data
    return JsonResponse({'code':0, 'data':{'zNodes':znode}, 'message':'ok'})


def update_menu(request):
    print request.POST.dict()
    return JsonResponse({'code':0, 'data':'', 'message':'修改成功'})
