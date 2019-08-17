# -*- coding: utf-8 -*-

from oms import settings
from rbac.models import *
from common.constant import constant

def const(request):
    return constant


def mysetting(request):
    return {
        'STATIC_URL': settings.STATIC_URL,
    }


def menu_list(request):    #获取该用户拥有的菜单，来做前端展示
    if not request.user.is_authenticated():
        return {
            'menu_list': []

        }


    #再获取整个菜单树
    data = []
    for i in TSysPermission.objects.filter(fparent_id=0).order_by('flocal'):
        accept = True

        if not TSysPermission.objects.filter(fparent_id=i.fid):  # 判断该一级节点有没有子节点
            data.append({
                'fid': i.fid, 'fname': i.fresource_name,
                 'fenable': i.favailable,
                'fmenu_icon': i.fmenu_icon, 'fresource_url': i.fresource_url, 'children': [],
                'accept':accept
            })
        else:   #有子节点
            level2_data = []
            for j in TSysPermission.objects.filter(fparent_id=i.fid).order_by('flocal'):        #遍历子节点

                children_accept = True
                level2_data.append({
                    'fid': j.fid, 'fname': j.fresource_name,
                     'fenable': j.favailable,
                    'fmenu_icon': j.fmenu_icon, 'fresource_url': j.fresource_url,
                    'accept': children_accept
                })
            data.append({
                'fid': i.fid, 'fname': i.fresource_name,
                 'children': level2_data,
                 'fenable': i.favailable,
                'fmenu_icon': i.fmenu_icon, 'fresource_url': i.fresource_url, 'accept':accept
            })

    return {
        'menu_list': data

    }

