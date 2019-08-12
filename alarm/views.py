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
from django.utils.decorators import classonlymethod
from django.views.generic.base import View
from django.conf.urls import include, url
from oms.views import BaseResView
from common.alarm import send_mail
from common.decorators import  login_exempt
from common.falcon import  Falcon, FalconResponse
from alarm.models import TMailServer
from oms import settings
from user_app.models import OmsUser
import traceback

class EventcaseView(BaseResView):
    def get(self, request):
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 30*86400  # 默认取1个月
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        return render(request, 'alarm/eventcase.html', locals())

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        fhostname = request.GET['fhostname']
        start_time = request.GET['start_time']
        end_time = request.GET['end_time']
        #将日期时间转换为时间戳
        start_timestamp = ''
        end_timestamp = ''
        if start_time:
            start_timestamp = int(time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S')))
        if end_time:
            end_timestamp = int(time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')))
        f = Falcon()
        #end_time = int(time.time())  # 必须要整形
        #start_time = end_time - 5 * 86400  # 30分钟
        if fhostname:
            endpoints = [fhostname]
        else:
            endpoints = []
        data = f.get_eventcase(startTime=start_timestamp, endTime=end_timestamp, endpoints=endpoints)
        data = data[
               (page - 1) * limit: page * limit]

        return  HttpResponse(json.dumps({'total':len(data), 'rows':data}))

    def detail(self, request):
        id = request.GET['id']
        return render(request, 'alarm/eventcase_detail.html', locals())


    def queryevent(self, request):
        id = request.GET['id']
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        f = Falcon()
        data = f.get_events(event_id=id)
        total = len(data)
        data = data[
               (page - 1) * limit: page * limit]
        return HttpResponse(json.dumps({'total': total, 'rows': data}))

class SenderView(BaseResView):

    def getMails(self):
        mail_list = []
        for i in OmsUser.objects.all():
            if i.is_active and i.email:
                mail_list.append(i.email)
        return ','.join(mail_list)

    @login_exempt
    def mail(self, request):
        print request.POST.dict()
        tos = request.POST['tos']
        subject = request.POST['subject']
        content = request.POST['content']
        #获取邮件服务器信息
        mailserver_obj = TMailServer.objects.first()
        if not mailserver_obj:
            return JsonResponse({'code':1, 'message':'邮箱服务器未设置', 'data':''})
        mail_host = mailserver_obj.fhost
        mail_user = mailserver_obj.fuser
        mail_pass = mailserver_obj.fpassword
        send_mail(mail_host,mail_user,mail_pass, tos, subject, content)
        return JsonResponse({'code':0, 'data':'', 'message':'发送成功'})



class HostGroupView(BaseResView):
    def get(self, request):

        return render(request, 'alarm/hostgroup.html', locals())

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        name = request.GET['name']
        f = Falcon()
        result = f.get_hostgroup_list(q=name)
        total = len(result)
        result = result[
               (page - 1) * limit: page * limit]
        data = []
        for i in result:
            data.append({'id':i['id'], 'name':i['grp_name'], 'create_user':i['create_user']})
        return  HttpResponse(json.dumps({'total':total, 'rows':data}))


    def templates(self, request):
        group_id = request.GET['id']
        f = Falcon()
        data = f.get_templates_of_hostgroup(group_id)
        hostgroup_info = data['hostgroup']
        data = data['templates']
        all_template_list = f.get_all_template_list()
        all_template_list = all_template_list['templates']
        return render(request, 'alarm/hostgroup_templates.html', locals())


    def unbind_template(self, request):
        template_id = int(request.POST['template_id'])
        hostgroup_id = int(request.POST['hostgroup_id'])
        f = Falcon()
        result = f.unbindTemplate2HostGroup(template_id, hostgroup_id)
        return FalconResponse(result)

    def bind_template(self, request):
        template_id = int(request.POST['template_id'])
        hostgroup_id = int(request.POST['hostgroup_id'])
        f = Falcon()
        result = f.bindTemplate2HostGroup(template_id, hostgroup_id)
        return FalconResponse(result)

    def delete(self, request):
        id = int(request.POST['id'])
        f = Falcon()
        result = f.delete_hostgroup(id)
        return FalconResponse(result)

    def update(self, request):
        hostgroup_id = int(request.POST['hostgroup_id'])
        hostgroup_name = request.POST['hostgroup_name']
        f = Falcon()
        result = f.update_hostgroup(hostgroup_id, hostgroup_name)
        return FalconResponse(result)

    def create(self, request):
        hostgroup_name = request.POST['hostgroup_name']
        f = Falcon(request.user.username)
        result =  f.create_hostgroup(hostgroup_name)
        return FalconResponse(result)


    def hosts(self, request):
        hostgroup_id = request.GET['id']
        f = Falcon()
        result = f.get_hostgroup_info_by_id(hostgroup_id)
        hostgroup_info = result['hostgroup']
        return render(request, 'alarm/hostgroup_hosts.html', locals())

    def get_hosts(self, request):
        try:
            limit = int(request.GET['limit'])
            page = int(request.GET['page'])
            name = request.GET['name']
            hostgroup_id = request.GET['hostgroup_id']
            f = Falcon()
            result = f.get_hostgroup_info_by_id(hostgroup_id)
            data = []
            for i in result['hosts']:
                if i['hostname'].find(name) >= 0:
                    data.append({'id':i['id'], 'hostname':i['hostname']})
            total = len(data)
            data = data[
                     (page - 1) * limit: page * limit]
        except:
            print traceback.format_exc()
        return HttpResponse(json.dumps({'total': total, 'rows': data}))

    def host_templates(self, request):
        host_id = request.GET['id']
        hostname = request.GET['hostname']
        f = Falcon()
        data = f.host_templates(host_id)
        return render(request, 'alarm/host_templates.html', locals())


    def host_hostgroups(self, request):
        host_id = request.GET['id']
        hostname = request.GET['hostname']
        f = Falcon()
        data = f.host_hostgroups(host_id)
        return render(request, 'alarm/host_hostgroups.html', locals())


    def host_unbind_hostgroup(self, request):
        host_id = int(request.POST['host_id'])
        hostgroup_id = int(request.POST['hostgroup_id'])
        f = Falcon()
        result = f.unbindHost2HostGroup(host_id, hostgroup_id)
        return FalconResponse(result)


    def host_add(self, request):
        hostgroup_id = request.GET['hostgroup_id']
        f = Falcon()
        result = f.get_hostgroup_info_by_id(hostgroup_id)
        hostgroup_info = result['hostgroup']
        return render(request, 'alarm/host_add.html', locals())

    def addhost(self, request):
        try:
            hostgroup_id = int(request.POST['hostgroup_id'])
            hostnames = request.POST['hostnames']
            #先统计该机器组现有的机器列表
            f = Falcon()
            result = f.get_hostgroup_info_by_id(hostgroup_id)
            hosts = result['hosts']
            hostname_list = [i['hostname'] for i in hosts]
            hostname_list +=  hostnames.strip().split()
            hostname_list = list(set(hostname_list))
            result = f.addHost2HhostGroup(hostgroup_id, hostname_list)
        except:
            print traceback.format_exc()
        return FalconResponse(result)

class TemplateView(BaseResView):

    def get(self, request):
        return render(request, 'alarm/template_list.html', locals())

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        name = request.GET['name']
        f = Falcon()
        result = f.get_all_template_list(q=name)
        result = result['templates']
        total = len(result)
        result = result[
                 (page - 1) * limit: page * limit]
        data = []
        for i in result:
            data.append({
                'tpl_name': i['template']['tpl_name'],
                'parent_name': i['parent_name'],
                'create_user': i['template']['create_user'],
                'id': i['template']['id']
            })
        return HttpResponse(json.dumps({'total': total, 'rows': data}))


    def update(self, request):
        template_id = request.GET['id']
        f = Falcon()
        hostgroups = f.get_hostgroups_of_template(template_id)  #当前模板下已关联的机器组
        current_hostgroup_ids = [i['id'] for i in hostgroups['hostgroups']]
        template_info = f.get_template_info(template_id)
        print template_info
        all_template_list = f.get_all_template_list()
        all_template_list = all_template_list['templates']
        print all_template_list
        all_hostgroup_list = f.get_all_hostgroup_list()
        op_list = ['==', '!=', '<', '<=', '>', '>=']
        cur_uic = template_info['action']['uic']
        cur_uic_list = cur_uic.split(',')
        all_uic = f.query_team()
        all_uic_list = [i['team']['name'] for i in all_uic]
        return render(request, 'alarm/template_update.html', locals())

    def view(self, request):
        template_id = request.GET['id']
        f = Falcon()
        hostgroups = f.get_hostgroups_of_template(template_id)  #当前模板下已关联的机器组
        current_hostgroup_ids = [i['id'] for i in hostgroups['hostgroups']]
        template_info = f.get_template_info(template_id)
        print template_info
        cur_uic = template_info['action']['uic']
        return render(request, 'alarm/template_view.html', locals())

    def get_strategy_info(self, request):
        strategy_id = request.POST['strategy_id']
        f = Falcon()
        strategy_info = f.get_strategy_info(strategy_id)
        return FalconResponse(strategy_info)


    def update_template(self, request):
        print request.POST.dict()
        template_id = int(request.POST['template_id'])
        parent_id = int(request.POST['parent_id'])
        name = request.POST['name']
        group_ids = request.POST.getlist('group_ids[]')
        #先更新模板基本信息
        f = Falcon(request.user.username)
        result = f.update_template(template_id, parent_id, name)
        if result.has_key('error'):
            return JsonResponse({'code':1, 'data':'', 'message':result['error']})
        #再更新机器组
        hostgroups = f.get_hostgroups_of_template(template_id)  # 当前模板下已关联的机器组
        old_hostgroup_ids = [i['id'] for i in hostgroups['hostgroups']]
        current_hostgroup_ids = [int(i) for i in group_ids]

        need_add_hostgroup_ids = list(set(current_hostgroup_ids).difference(old_hostgroup_ids))
        need_remove_hostgroup_ids = list(set(old_hostgroup_ids).difference(current_hostgroup_ids))
        for i in need_add_hostgroup_ids:
            f.bindTemplate2HostGroup(template_id, i)
        for i in need_remove_hostgroup_ids:
            f.unbindTemplate2HostGroup(template_id, i)
        return JsonResponse({'code':0, 'data':'', 'message':'ok'})


    def create_strategy(self, request):
        f = Falcon(request.user.username)
        result = f.create_strategy(**request.POST.dict())
        return FalconResponse(result)


    def update_strategy(self, request):
        f = Falcon(request.user.username)
        result = f.update_strategy(**request.POST.dict())
        return FalconResponse(result)


    def create_action(self, request):
        data = request.POST.dict()
        data['uic'] = ','.join(request.POST.getlist('uic[]'))
        data.pop('uic[]')
        f = Falcon(request.user.username)
        result = f.create_action(**data)
        return FalconResponse(result)


    def update_action(self, request):
        data =  request.POST.dict()
        data['uic'] = ','.join(request.POST.getlist('uic[]'))
        data.pop('uic[]')
        f = Falcon(request.user.username)
        result =  f.update_action(**data)
        return FalconResponse(result)


    def create(self, request):   #创建模板
        template_name = request.POST['template_name']
        f = Falcon(request.user.username)
        result = f.create_template(template_name)
        return FalconResponse(result)


class ExpressionView(BaseResView):

    def get(self, request):
        return render(request, 'alarm/expression_list.html', locals())

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        name = request.GET['name']
        f = Falcon()
        result = f.get_all_expression_list()
        print result
        total = len(result)
        data = []
        for i in  result:
            if i['expression'].find(name) >= 0:
                data.append(i)
        data = data[
                 (page - 1) * limit: page * limit]

        return HttpResponse(json.dumps({'total': total, 'rows': data}))


    def add(self, request):     #创建/更新的页面
        id = request.GET.get('id', 0)
        f = Falcon(request.user.username)
        expression_info = f.get_expression_info_by_id(id)
        print expression_info
        op_list = ['==', '!=', '<', '<=', '>', '>=']
        current_uic_list = expression_info['action']['uic'].split(',')
        all_uic = f.query_team()
        all_uic_list = [i['team']['name'] for i in all_uic]

        return render(request, 'alarm/expression_add.html', locals())


    def create(self, request):
        f = Falcon()
        result = f.create_expression(**request.POST.dict())
        return FalconResponse(result)

    def update(self, request):
        data = json.loads(request.body)
        f = Falcon()
        result = f.update_expression(**data)
        return FalconResponse(result)

    def delete(self, request):
        try:
            id = request.POST['id']
            print id
            f = Falcon()
            result = f.delete_expression(id)
        except:
            print traceback.format_exc()
        return FalconResponse(result)