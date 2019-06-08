# -*- coding: utf-8 -*-

from oms import settings
from rbac.models import *


def mysetting(request):
    return {
        'STATIC_URL': settings.STATIC_URL,
    }


def menu_list(request):    #获取该用户拥有的菜单，来做前端展示
    request.user
    if not request.user.is_authenticated():
        return {
            'menu_list': []

        }
    accept_menu_id_list = []     #先获取该用户可以访问哪些菜单ID
    role_list = request.user.tsysrole_set.all()
    for role_obj in role_list:
        for permisson_obj in role_obj.permissions.all():
            accept_menu_id_list.append(permisson_obj.fid)
    accept_menu_id_list = list(set(accept_menu_id_list))

    #再获取整个菜单树
    data = []
    for i in TSysPermission.objects.filter(fparent_id=0).order_by('flocal'):
        if i.fid in accept_menu_id_list:
            accept = True
        else:
            accept = False
        if not TSysPermission.objects.filter(fparent_id=i.fid):  # 判断该一级节点有没有子节点
            data.append({
                'fid': i.fid, 'fname': i.fresource_name,
                 'fenable': i.favailable,
                'ficon': i.fmenu_icon, 'fresource_url': i.fresource_url, 'children': [],
                'accept':accept
            })
        else:   #有子节点
            level2_data = []
            for j in TSysPermission.objects.filter(fparent_id=i.fid).order_by('flocal'):        #遍历子节点
                children_accept = False
                if j.fid in accept_menu_id_list:
                    children_accept = True
                level2_data.append({
                    'fid': j.fid, 'fname': j.fresource_name,
                     'fenable': j.favailable,
                    'ficon': j.fmenu_icon, 'fresource_url': j.fresource_url,
                    'accept': children_accept
                })
            data.append({
                'fid': i.fid, 'fname': i.fresource_name,
                 'children': level2_data,
                 'fenable': i.favailable,
                'ficon': i.fmenu_icon, 'fresource_url': i.fresource_url, 'accept':accept
            })

    return {
        'menu_list': data

    }

