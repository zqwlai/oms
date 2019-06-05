#coding: UTF-8 -*-

from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from  service_app.models import Service
import time
import json
from common.falcon import Falcon
from oms import settings
import traceback

def service_list(request):
    return render(request, 'service/list.html',{'root_node':'service','child_node':'list'})


def query_service(request):
    limit = int(request.GET['limit'])
    page = int(request.GET['page'])
    Fhost = request.GET['Fhost']
    Fname = request.GET['Fname']
    Fport = request.GET['Fport']
    Fcluster = request.GET['Fcluster']
    query_dict = {}
    if Fhost:
        query_dict.update({'Fhost__contains': Fhost})
    if Fname:
        query_dict.update({'Fname__contains': Fname})
    if Fport:
        query_dict.update({'Fport__contains': Fport})

    if Fcluster:
        query_dict.update({'Fclusterr__contains': Fcluster})

    data = Service.objects.filter(**query_dict)[(page-1)*limit: page*limit]
    total = Service.objects.filter(**query_dict).count()
    result = []
    for i in data:
        result.append({'Fid':i.Fid, 'Fcluster':i.Fcluster,'Fhost':i.Fhost, 'Fname':i.Fname, 'Fport':i.Fport,'Fdesc':i.Fdesc, 'Fcreate_time': str(i.Fcreate_time)})
    return HttpResponse(json.dumps({'total':total, 'rows': result}))



def add_service(request):
    Fhost = request.POST['Fhost']
    Fname = request.POST['Fname']
    Fport = request.POST['Fport']
    Fdesc = request.POST['Fdesc']
    Fcluster = request.POST['Fcluster']
    #判断服务是否已经存在
    if Service.objects.filter(Fhost=Fhost,Fname=Fname,Fport=Fport,Fcluster=Fcluster):
        return JsonResponse({'code':1, 'data':'', 'message':'集群%s-主机%s-服务%s-端口%s已经存在！'%(Fcluster, Fhost, Fname, Fport)})
    s = Service.objects.create(Fhost=Fhost,Fname=Fname,Fport=Fport,Fcluster=Fcluster)
    return JsonResponse({'code':0, 'data':'', 'message':'服务创建成功！'})



def delete_service(request):
    Fid = request.POST['id']
    Service.objects.filter(Fid=Fid).delete()
    return JsonResponse({'code':0, 'data':'', 'message':'服务删除成功！'})


def query_status(request):
    limit = int(request.GET['limit'])
    page = int(request.GET['page'])
    Fhost = request.GET['Fhost']
    Fname = request.GET['Fname']
    Fport = request.GET['Fport']
    Fcluster = request.GET['Fcluster']
    data = Service.objects.filter(Fcluster__contains=Fcluster, Fhost__contains=Fhost, Fname__contains=Fname, Fport__contains=Fport)[
           (page - 1) * limit: page * limit]
    total = Service.objects.filter(Fcluster__contains=Fcluster, Fhost__contains=Fhost, Fname__contains=Fname, Fport__contains=Fport).count()
    result = []
    for i in data:
        result.append({
            'Fid': i.Fid,
            'Fcluster':i.Fcluster,
            'Fhost': i.Fhost,
            'Fname': i.Fname,
            'Fport': i.Fport,
            'Fdesc': i.Fdesc,
            'Fcreate_time': str(i.Fcreate_time),
            'Fstatus': i.Fstatus
        })
    return HttpResponse(json.dumps({'total': total, 'rows': result}))


def status(request):
    return render(request, 'service/status.html', {'root_node':'service','child_node':'monitor'})


def graph(request):
    cluster = request.GET['cluster']
    service = request.GET['service']
    host = request.GET['host']
    port = request.GET['port']
    end_timestamp = int(time.time())
    start_timestamp = end_timestamp - 3600      #默认取1个小时
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_timestamp))
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
    print end_time
    root_node = 'service'
    child_node = 'monitor'
    return render(request, 'service/graph.html', locals())


def update(request):
    if request.method == 'GET':
        id = request.GET['id']
        service_obj = Service.objects.get(Fid=id)
        return render(request, 'service/update.html',{'service_obj':service_obj, 'root_node':'service', 'child_node':'list'})
    else:
        Fid = request.POST['Fid']
        Fhost = request.POST['Fhost']
        Fname = request.POST['Fname']
        Fport = request.POST['Fport']
        Fdesc = request.POST['Fdesc']
        Fcluster = request.POST['Fcluster']
        # 判断服务是否已经存在
        if Service.objects.filter(Fhost=Fhost, Fname=Fname, Fport=Fport, Fcluster=Fcluster).exclude(Fid=Fid):
            return JsonResponse({'code': 1, 'data': '', 'message': '集群%s-主机%s-服务%s-端口%s已经存在！' % (Fcluster, Fhost, Fname, Fport)})
        Service.objects.filter(Fid=Fid).update(Fcluster=Fcluster, Fhost=Fhost, Fname=Fname, Fport=Fport, Fdesc=Fdesc)
        return JsonResponse({'code': 0, 'data': '', 'message': '服务修改成功！'})



def query_graph(request):
    host = request.POST['host']
    service = request.POST['service']
    port = request.POST['port']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    start_timestamp = int(time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')))
    end_timestamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))
    f = Falcon()
    counter = '%s/port=%s' % (settings.port_listen_key, port)
    history_data = f.get_history_data(start_timestamp, end_timestamp, [host], [counter], CF='AVERAGE')
    data = history_data[0]['Values']
    print data
    #data.reverse()
    time_list = []
    value_list = []
    for i in data:
        time_list.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['timestamp']) ))
        value_list.append(i['value'])

    return JsonResponse({'code':0, 'data':{'time_list':time_list,'value_list':value_list}, 'message':'ok'})



def getport(request):
    host = request.POST['host']
    port_list = [ i.Fport for i in Service.objects.filter(Fhost=host) ]
    return JsonResponse({'code':0, 'data':{'port_list':port_list}, 'message':'ok'})
