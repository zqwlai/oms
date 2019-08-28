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
from service_app.models import Service
from docker.models import VirtualMachine
from common.falcon import Falcon
from oms import  settings
from common.utils import  get_local_ip, gen_tags
from common.calc import get_cluster_available
import traceback
import logging
logger_500 = logging.getLogger("500")
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class BaseResView(View):

    @classonlymethod
    def urls(cls, **initkwargs):
        name = cls.__name__
        # 去掉类名中的view
        name = name.lower().replace('view', '')
        instance = cls(**initkwargs)
        urls = []
        urls.append(url(r'^%s$' % name, cls.as_view()))
        for k, v in cls.__dict__.iteritems():
            if not k.startswith('_'):
                urls.append(url(r'^%s/%s/$' %
                                (name, k), getattr(instance, k)))
                urls.append(url(r'^%s/%s$' %
                                (name, k), getattr(instance, k)))
        return urls


def index(request):
    return HttpResponseRedirect('/dashboard/main')


def process_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        # isadmin=is_admin(request.user)
        return HttpResponseRedirect('/dashboard/main')
    else:
        return render(request, 'login.html', {'err': '用户名或密码不正确！'})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register(request):
    return render(request, 'register.html')


def process_register(request):
    username = request.POST['username']
    password = request.POST['password']
    cname = request.POST['cname']
    email = request.POST['email']

    f = Falcon()
    ret = f.register(username, password, cname, email)
    if ret.has_key('error'):
        return JsonResponse({'code':1, 'data':'', 'message':ret['error']})

    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)
    return JsonResponse({'code':0, 'data':'', 'message':'用户注册成功!'})



def handler_404(request):
    if request.is_ajax() or request.method == 'POST':
        result = {'code': 1,
            'data': '',
            'message':'您所请求的内容不存在'}
        return JsonResponse(result)
    else:
        return render(request, '404.html')



def handler_500(request):
    logger_500.error('%s %s'%(request.request_id, traceback.format_exc()))

    if request.is_ajax() or request.method == 'POST':
        error_message = traceback.sys.exc_value.message
        if isinstance(error_message, tuple):
            result = {'code':error_message[0], 'message':error_message[1] ,'data':''}
        else:
            result = {'code':5000, 'data':'', 'message':traceback.format_exc()}
        return JsonResponse(result)
    return render(request, '500.html')



def getcomponent(request):  #获取对应主机下所有的组件信息
    result = Service.objects.values('fhost', 'fport', 'fname', 'fadmin_user', 'fadmin_password').distinct()
    data = [{'fhost': i['fhost'], 'fport':i['fport'], 'fname':i['fname'], 'fadmin_user':i['fadmin_user'], 'fadmin_password':i['fadmin_password'] } for i in result]
    return JsonResponse({'code':0, 'data':data, 'message':'ok'})

def getContainer(request):
    data = {}
    for i in VirtualMachine.objects.all():
        if i.fmaster in data:
            data[i.fmaster].append(i.fhostname)
        else:
            data[i.fmaster] = [i.fhostname]
    return JsonResponse({'code': 0, 'data': data, 'message': 'ok'})


def addContainer(request):
    fhostname = request.POST['fhostname']
    fmaster = request.POST['fmaster']
    fip = request.POST.get('fip', '')
    if not VirtualMachine.objects.filter(fhostname=fhostname, fmaster=fmaster):
        VirtualMachine.objects.create(fhostname=fhostname, fmaster=fmaster, fip=fip)
    return JsonResponse({'code': 0, 'data': '', 'message': 'ok'})



def query_cluster_status(request):    #统计每个集群的可用性
    try:
        cluster = request.POST['cluster']
        range = request.POST['range']
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - int(range)
        #先统计有哪些集群名
        #cluster_list = [i['fcluster'] for i in Service.objects.values('fcluster').distinct() if i['fcluster']]
        cluster_list = [cluster]
        counters = ['cluster.available.percent/clusterName=%s,project=oms'%i for i in cluster_list]
        endpoint = get_local_ip()
        f = Falcon()
        history_data = f.get_history_data(start_timestamp, end_timestamp, [endpoint], counters, step=24*60*60, CF='AVERAGE')
        data = []
        for i in history_data:
            tags = i['counter'].split('/')[1]
            tag_dict = gen_tags(tags)
            cluster = tag_dict.get('clusterName')
            ts_value = []
            c_date = time.strftime("%Y-%m-%d")
            c_timestamp = int(time.mktime(time.strptime(c_date, '%Y-%m-%d'))) * 1000
            for j in i['Values']:
                if (j['timestamp'] - 8*60*60)*1000 == c_timestamp:
                    ts_value.append([c_timestamp, get_cluster_available(cluster, c_date)])
                else:
                    ts_value.append([(j['timestamp'] - 8*60*60)*1000, j['value']])  #这里要减去8个小时，是因为rrd里存的点的时刻是8点钟

            data.append({'data':ts_value, 'name':cluster})
    except:
        print traceback.format_exc()
    return JsonResponse({'code': 0, 'data': data, 'message': 'ok'})


def query_service_top(request):
    range = request.POST['range']
    topn = int(request.POST['topn'])
    end_timestamp = int(time.time())
    start_timestamp = end_timestamp - int(range)
    #先统计有endporints和couters
    endpoints = []
    ports = []
    for i in Service.objects.all():
        if i.fhost:
            endpoints.append(i.fhost)
        if i.fport:
            ports.append(i.fport)
    endpoints = list(set(endpoints))
    ports = list(set(ports))
    counters = ['%s/port=%s,project=oms'%(settings.port_listen_key, i) for i in ports]
    f = Falcon()
    history_data = f.get_history_data(start_timestamp, end_timestamp, endpoints, counters, step=60, CF='AVERAGE')
    names = []
    values = []
    data = {}
    for i in history_data:
        if i['Values']:
            host = i['endpoint']
            tags = i['counter'].split('/')[1]
            tag_dict = gen_tags(tags)
            port = tag_dict['port']
            #计算故障率
            fail_count = 0
            for j in i['Values']:
                if j['value'] == 0:
                    fail_count += 1
            fail_rate = '%.2f'%(float(fail_count)/len(i['Values'])*100)
            fail_rate = float(fail_rate)
            data['%s:%s'%(host, port)] = fail_rate
        #排序
    data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:topn]
    for k, v in data:
        names.append(k)
        values.append(v)
    print values
    return JsonResponse({'code': 0, 'data': {'names':names, 'values':values}, 'message': 'ok'})


class DashboardView(BaseResView):
    def main(self, request):
        # 统计集群数，服务数、机器数
        cluster_count = Service.objects.values('fcluster').distinct().count()
        service_count = Service.objects.values('fhost', 'fname', 'fport').distinct().count()
        host_count = Service.objects.values('fhost').distinct().count()

        # 统计每个集群的健康度
        status_info = []

        cluster_list = []
        success_rate_list = []
        series = []
        success_num_list = []
        unknow_num_list = []
        fail_num_list = []
        for i in Service.objects.values('fcluster').distinct():
            fcluster = i['fcluster']
            cluster_list.append(fcluster)

            success_num = int(Service.objects.filter(fcluster=fcluster, fstatus=1).count())
            unknow_num = int(Service.objects.filter(fcluster=fcluster, fstatus=0).count())
            fail_num = int(Service.objects.filter(fcluster=fcluster, fstatus=2).count())
            total = success_num + unknow_num + fail_num

            success_num_list.append(success_num)
            unknow_num_list.append(unknow_num)
            fail_num_list.append(fail_num)
            if total == 0:
                success_rate = 100
            else:
                success_rate = '%.2f' % (float(success_num) / total * 100)
                success_rate = float(success_rate)
            success_rate_list.append(success_rate)
            status_info.append({'fcluster': fcluster, 'success_num': success_num, 'unknow_num': unknow_num,
                                'fail_num': fail_num, 'total_num': success_num + unknow_num + fail_num})

        # 统计最近10次的告警事件
        host_list = [i['fhost'] for i in Service.objects.values('fhost').distinct()]
        for i in VirtualMachine.objects.all():
            host_list.append(i.fhostname)
        host_list = list(set(host_list))
        if not host_list:
            eventcase_list = []
        else:
            f = Falcon()
            eventcase_list = f.get_eventcase(endpoints=host_list)
            eventcase_list = eventcase_list[0:10]
        # print eventcase_list
        return render(request, 'dashboard.html', locals())

    def servicetop(self, request):
        cluster = request.GET.get('cluster', '')
        ts = request.GET.get('ts')
        if not ts:
            date = time.strftime('%Y-%m-%d')
        else:
            x = time.localtime(float(ts))
            date = time.strftime('%Y-%m-%d', x)

        cluster_list = [i['fcluster'] for i in Service.objects.values('fcluster').distinct()]
        print cluster_list
        return  render(request, 'service_top.html', locals())


    def query_service_top(self, request):
        try:
            cluster = request.POST['cluster']
            date = request.POST['date']
            topn = int(request.POST['topn'])
            start_ts = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
            end_ts = start_ts + 86400
            #先插集群下有哪些ip和端口
            endpoints = []
            ports = []
            for i in Service.objects.filter(fcluster=cluster):
                if i.fhost:
                    endpoints.append(i.fhost)
                if i.fport:
                    ports.append(i.fport)
            endpoints = list(set(endpoints))
            ports = list(set(ports))
            counters = ['%s/port=%s,project=oms' % (settings.port_listen_key, i) for i in ports]
            f = Falcon()
            history_data = f.get_history_data(start_ts, end_ts, endpoints, counters, step=60, CF='AVERAGE')
            print history_data
            names = []
            values = []
            data = {}
            for i in history_data:
                if i['Values']:
                    host = i['endpoint']
                    tags = i['counter'].split('/')[1]
                    tag_dict = gen_tags(tags)
                    port = tag_dict['port']
                    if not Service.objects.filter(fhost=host,fport=port,fcluster=cluster):
                        continue
                    # 计算故障率
                    fail_count = 0
                    for j in i['Values']:
                        if j['value'] == 0:
                            fail_count += 1
                    fail_rate = '%.2f' % (float(fail_count) / len(i['Values']) * 100)
                    fail_rate = float(fail_rate)
                    data['%s:%s' % (host, port)] = fail_rate
                # 排序
            if data:
                print data
                data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:topn]
                for k, v in data:
                    names.append(k)
                    values.append(v)
        except:
            print traceback.format_exc()
        return JsonResponse({'code': 0, 'data': {'names': names, 'values': values}, 'message': 'ok'})

    def port(self, request):
        host = request.GET.get('host', '')
        port = request.GET.get('port', '')
        date = request.GET.get('date')
        if not date:
            c_ts = int(time.time())
            start_time = time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(c_ts-3600))     #1小时前
            end_time = time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(c_ts))
        else:

            start_ts = int(time.mktime(time.strptime(date, '%Y-%m-%d')))
            end_ts = start_ts + 86400
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_ts))
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_ts))
        return  render(request, 'port.html', locals())


    def query_port(self, request):
        host = request.POST['host']
        port = request.POST['port']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        start_ts = int(time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S')))
        end_ts = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')))
        counter = '%s/port=%s,project=oms'%(settings.port_listen_key, port)
        f = Falcon()
        history_data = f.get_history_data(start_ts, end_ts, [host], [counter], CF='AVERAGE')
        hdata = []
        for i in history_data:
            hdata.append({'name': i['endpoint'], 'data': [[j['timestamp'] * 1000, j['value']] for j in i['Values']]})
        return JsonResponse({'code': 0, 'data': {'hdata': hdata}, 'message': 'ok'})





