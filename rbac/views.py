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
from common.falcon import Falcon
from oms import settings
import traceback
from oms.views import BaseResView
from alarm.models import TMailServer
from common.alarm import check_mailserver

class MailSettingsView(BaseResView):
    def get(self, request):
        mailserver_obj = TMailServer.objects.first()
        return render(request, 'rbac/mailsettings.html', locals())

    def check(self, request):
        user = request.POST['user']
        password = request.POST['password']
        host = request.POST['host']
        return  JsonResponse( {'code':0, 'data':check_mailserver(host, user, password), 'message':''})

    def update(self, request):
        user = request.POST['user']
        password = request.POST['password']
        host = request.POST['host']
        mailserver_obj = TMailServer.objects.first()
        if mailserver_obj:
            mailserver_obj.fuser = user
            mailserver_obj.fpassword = password
            mailserver_obj.fhost = host
            mailserver_obj.save()
        else:
            TMailServer.objects.create(fuser=user, fpassword=password, fhost=host)
        return     JsonResponse( {'code':0, 'data':'', 'message':'更新成功'})

class MenuView(BaseResView):
    def get(self, request):
        return render(request, 'rbac/menu_list.html', locals())

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

        return render(request, 'rbac/sysuser.html', locals())

    def data(self, request):
        username = request.GET['username']
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        data = OmsUser.objects.filter(username__contains=username)[(page - 1) * limit: page * limit]
        total = OmsUser.objects.filter(username__contains=username).count()
        result = []
        for i in data:
            result.append({
                'id': i.id,
                'username': i.username,
                'phone': i.phone,
                'email':i.email,
                'is_active':i.is_active,
                'role':i.role,
                'cname': i.cname
            })

        return HttpResponse(json.dumps({'total': total, 'rows': result}))

    def get_user_obj(self, request):
        id = request.POST['id']
        user_obj = OmsUser.objects.get(id=id)
        if user_obj.is_active:
            status = 1
        else:
            status = 0
        data = {
            'phone': user_obj.phone,
            'email': user_obj.email,
            'status': status,
            'username': user_obj.username
        }

        return JsonResponse({'code':0, 'data':data, 'message':'ok'})

    def update(self, request):
        id = request.POST['id']
        status = request.POST['status']
        phone = request.POST['phone']
        email = request.POST['email']
        user_obj = OmsUser.objects.get(id=id)
        user_obj.is_active = int(status)
        user_obj.phone = phone
        user_obj.email = email
        user_obj.save()
        #同时更新falcon用户
        f = Falcon()
        f.update_user(user_obj.cname, email, phone, qq='')
        return JsonResponse({'code': 0, 'data': '', 'message': '更新成功'})


    def delete(self, request):
        id = request.POST['id']
        OmsUser.objects.filter(id=id).delete()
        return JsonResponse({'code': 0, 'data': '', 'message': '删除成功'})



class RoleView(BaseResView):
    def get(self, request):
        f = Falcon()
        user_list = f.get_user_list()
        return render(request, 'rbac/role.html', locals())


    def data(self, request):
        name = request.GET['name']
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])

        f = Falcon()
        data = f.query_team(q=name)
        print data
        total = len(data)
        data = data[(page - 1) * limit: page * limit]
        result = []
        for i in data:
            result.append({'id': i['team']['id'], 'name': i['team']['name'], 'resume':i['team']['resume'],'creator_name': i['creator_name']})
        return HttpResponse(json.dumps({'total': total, 'rows': result}))


    def get_role_info(self, request):
        try:
            id = request.POST['id']
            f = Falcon()
            team_info  = f.get_team_info_by_id(id)
            name = team_info['name']
            resume = team_info['resume']
            user_id_list = [int(i['id']) for i in team_info['users']]
            data = {'name':name, 'resume':resume, 'user_id_list':user_id_list}
        except:
            print traceback.format_exc()
        return JsonResponse({'code':0, 'data':data, 'message':'ok'})

    def delete(self, request):
        id = request.POST['id']
        f = Falcon()
        print f.delete_team(id)
        return JsonResponse({'code': 0, 'data': '', 'message': '删除成功'})

    def add(self, request):
        name = request.POST['name']
        resume = request.POST['resume']
        user_list = request.POST.getlist('users')
        user_list = [int(i) for i in user_list]
        f = Falcon(request.user.username)
        print f.create_team(name, resume, user_list)
        return JsonResponse({'code': 0, 'data': '', 'message':'用户组【%s】创建成功'%name})

    def update(self, request):
        id = int(request.POST['id'])
        name = request.POST['resume']
        resume = request.POST['resume']
        user_id_list = request.POST.getlist('users')
        user_id_list = [int(i) for i in user_id_list]
        f = Falcon()
        print f.update_team(id, name, resume, user_id_list)
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
                if i.fresource_url == '/dashboard':     #dashboard菜单栏禁用checkbox，同时选中该节点
                    chkDisabled = 'true'
                    checked = True
                else:
                    chkDisabled = 'false'
                    checked = False
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

