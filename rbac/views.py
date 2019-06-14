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
from rbac.models import TSysPermission, TSysRole
from user_app.models import OmsUser
from oms import settings
import traceback
from oms.views import BaseResView



class MenuView(BaseResView):
    def get(self, request):
        return render(request, 'rbac/menu_list.html',{'root_node':'rbac','child_node':'menu'})

    def update(self, request):
        print request.POST.dict()
        try:
            fid = request.POST['fid']
            args = request.POST.dict()
            args.pop('fid')
            TSysPermission.objects.filter(fid=fid).update(**args)
        except:
            print traceback.format_exc()
        return JsonResponse({'code': 0, 'data': '', 'message': '修改成功'})

    def data(self, request):
        znode = [{'fid': 0, 'name': '导航菜单', 'open': 'true', 'children': []}]

        data = []
        for i in TSysPermission.objects.filter(fparent_id=0).order_by('flocal'):
            if not TSysPermission.objects.filter(fparent_id=i.fid):  # 判断该一级节点有没有子节点
                data.append({
                    'fid': int(i.fid), 'name': i.fresource_name, 'open': 'true',
                    'isParent': 'true', 'flocal': int(i.flocal), 'favailable': int(i.favailable),
                    'fmenu_icon': str(i.fmenu_icon), 'fresource_url': str(i.fresource_url), 'children': []
                })
            else:
                level2_data = []
                for j in TSysPermission.objects.filter(fparent_id=i.fid).order_by('flocal'):  # 遍历子节点
                    level2_data.append({
                        'fid': int(j.fid), 'name': j.fresource_name,
                        'flocal': int(j.flocal), 'favailable': int(j.favailable),
                        'fmenu_icon': str(j.fmenu_icon), 'fresource_url': str(j.fresource_url)
                    })
                data.append({
                    'fid': int(i.fid), 'name': i.fresource_name,
                    'open': 'true', 'isParent': 'true', 'children': level2_data,
                    'flocal': int(i.flocal), 'favailable': int(i.favailable),
                    'fmenu_icon': str(i.fmenu_icon), 'fresource_url': str(i.fresource_url)
                })
        znode[0]['children'] = data
        return JsonResponse({'code': 0, 'data': {'zNodes': znode}, 'message': 'ok'})

    def add(self, request):
        try:

            args = request.POST.dict()
            print args
            fresource_name = args['fresource_name']
            fresource_url = args['fresource_url']
            if TSysPermission.objects.filter(fresource_name = fresource_name):
                return JsonResponse({'code':1, 'data':'', 'message':'菜单名已存在'})
            if TSysPermission.objects.filter(fresource_url= fresource_url):
                return JsonResponse({'code': 1, 'data': '', 'message': '访问链接已经存在'})
            TSysPermission.objects.create(**args)
        except:
            print traceback.format_exc()
        return JsonResponse({'code': 0, 'data': '', 'message': '新建成功'})


    def delete(self, request):
        fid = request.POST['fid']
        TSysPermission.objects.filter(fid=fid).delete()

        return JsonResponse({'code': 0, 'data': '', 'message': '删除成功'})


class UserView(BaseResView):
    def get(self, request):
        role_list = TSysRole.objects.all()
        return render(request, 'rbac/sysuser.html', {'role_list': role_list})

    def data(self, request):
        username = request.GET['username']
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        data = OmsUser.objects.filter(username__contains=username)[(page - 1) * limit: page * limit]
        total = OmsUser.objects.filter(username__contains=username).count()
        result = []
        for i in data:
            role_id_list = [str(j.fid) for j in i.tsysrole_set.all()]
            roleids = '|'.join(role_id_list)
            result.append({'id': i.id, 'username': i.username, 'phone': i.phone, 'email':i.email, 'is_active':i.is_active, 'roleids':roleids})

        return HttpResponse(json.dumps({'total': total, 'rows': result}))

    def update(self, request):
        id = request.POST['edit_id']
        status = request.POST['edit_status']
        role_list = request.POST.getlist('edit_role')
        user_obj = OmsUser.objects.get(id=id)
        user_obj.is_active = status
        user_obj.save()

        #获取原先的权限列表
        old_role_list = [i.id for i in user_obj.tsysrole_set.all()]

        #需要增加的权限
        need_add_role_list = list(set(role_list).difference(old_role_list))
        print need_add_role_list
        for i in need_add_role_list:
            user_obj.tsysrole_set.add(i)
        #需要删除的权限
        need_remove_role_list = list(set(old_role_list).difference(role_list))
        for i in need_remove_role_list:
            user_obj.tsysrole_set.remove(i)
        user_obj.save()

        return JsonResponse({'code': 0, 'data': '', 'message': '更新成功'})


class RoleView(BaseResView):
    def get(self, request):
        return render(request, 'rbac/role.html', {'root_node':'rbac','child_node':'role'})


    def data(self, request):
        fname = request.GET['fname']
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        data = TSysRole.objects.filter(fname__contains=fname)[(page - 1) * limit: page * limit]
        total = TSysRole.objects.filter(fname__contains=fname).count()
        result = []
        for i in data:
            result.append({'fid': i.fid, 'fname': i.fname, 'fcreate_time': str(i.fcreate_time)})
        return HttpResponse(json.dumps({'total': total, 'rows': result}))

    def delete(self, request):
        fid = request.POST['fid']
        TSysRole.objects.filter(fid=fid).delete()
        return JsonResponse({'code': 0, 'data': '', 'message': '删除成功'})

    def add(self, request):
        fname = request.POST['fname']
        if TSysRole.objects.filter(fname=fname):
            return JsonResponse({'code': 1, 'data': '', 'message':'角色名已经存在'})
        TSysRole.objects.create(fname=fname)
        return JsonResponse({'code': 0, 'data': '', 'message':'角色【%s】创建成功'%fname})

    def update(self, request):
        fid = request.POST['edit_fid']
        fname = request.POST['edit_fname']
        if TSysRole.objects.filter(fname=fname).exclude(fid=fid):
            return JsonResponse({'code': 1, 'data': '', 'message':'角色名已经存在'})
        TSysRole.objects.filter(fid=fid).update(fname=fname)
        return JsonResponse({'code': 0, 'data': '', 'message': '角色更新成功'})

    def permission(self, request):      #获取该角色有哪些菜单权限
        fid = request.POST['fid']
        role_obj = TSysRole.objects.get(fid=fid)
        accept_menu_id_list = [i.fid for i in role_obj.permissions.all()]
        data = []
        for i in TSysPermission.objects.filter(fparent_id=0).order_by('flocal'):
            if i.fid in accept_menu_id_list:
                checked = True
            else:
                checked = False
            if not TSysPermission.objects.filter(fparent_id=i.fid):  # 判断该一级节点有没有子节点
                if i.fresource_url == '/dashboard':     #dashboard菜单栏禁用checkbox
                    chkDisabled = 'true'
                else:
                    chkDisabled = 'false'
                data.append({
                    'fid': i.fid, 'name': i.fresource_name,
                    'fenable': i.favailable,
                    'ficon': i.fmenu_icon, 'fresource_url': i.fresource_url, 'children': [],
                    'checked': checked, 'open':'true', 'chkDisabled':chkDisabled
                })
            else:  # 有子节点
                level2_data = []
                for j in TSysPermission.objects.filter(fparent_id=i.fid).order_by('flocal'):  # 遍历子节点
                    children_accept = False
                    if j.fid in accept_menu_id_list:
                        children_accept = True
                    level2_data.append({
                        'fid': j.fid, 'name': j.fresource_name,
                        'fenable': j.favailable,
                        'ficon': j.fmenu_icon, 'fresource_url': j.fresource_url,
                        'checked': children_accept
                    })
                data.append({
                    'fid': i.fid, 'name': i.fresource_name,
                    'children': level2_data,
                    'fenable': i.favailable,
                    'ficon': i.fmenu_icon, 'fresource_url': i.fresource_url, 'checked': checked, 'open':'true'
                })

        return JsonResponse({'code':0, 'data':{'zNodes':data,}, 'message':'ok'})



    def updateauth(self, request):
        checked_id_list =  request.POST.getlist('checked_id_list[]')
        fid = request.POST['fid']       #获取角色id
        role_obj = TSysRole.objects.get(fid=fid)
        #获取老的菜单id
        old_menu_id = [str(i.fid) for i in  role_obj.permissions.all()]
        need_add_menu_ids = list(set(checked_id_list).difference(old_menu_id))
        need_remove_menu_ids = list(set(old_menu_id).difference(checked_id_list))
        for i in need_add_menu_ids:
            role_obj.permissions.add(i)
        for i in   need_remove_menu_ids:
            role_obj.permissions.remove(i)
        return JsonResponse({'code':0, 'data':'', 'message':'更新成功'})

