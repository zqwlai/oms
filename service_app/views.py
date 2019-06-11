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
from oms.views import BaseResView


class ConfView(BaseResView):
    def get(self, request):
        return render(request, 'service/list.html')

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        fhost = request.GET['fhost']
        fname = request.GET['fname']
        fport = request.GET['fport']
        fcluster = request.GET['fcluster']
        query_dict = {}
        if fhost:
            query_dict.update({'fhost__contains': fhost})
        if fname:
            query_dict.update({'fname__contains': fname})
        if fport:
            query_dict.update({'fport__contains': fport})

        if fcluster:
            query_dict.update({'fclusterr__contains': fcluster})

        data = Service.objects.filter(**query_dict)[(page - 1) * limit: page * limit]
        total = Service.objects.filter(**query_dict).count()
        result = []
        for i in data:
            result.append({'fid': i.fid, 'fcluster': i.fcluster, 'fhost': i.fhost, 'fname': i.fname, 'fport': i.fport,
                           'fdesc': i.fdesc, 'fcreate_time': str(i.fcreate_time)})
        return HttpResponse(json.dumps({'total': total, 'rows': result}))


    def add(self, request):
        fhost = request.POST['fhost']
        fname = request.POST['fname']
        fport = request.POST['fport']
        fdesc = request.POST['fdesc']
        fcluster = request.POST['fcluster']
        # 判断服务是否已经存在
        if Service.objects.filter(fhost=fhost, fname=fname, fport=fport, fcluster=fcluster):
            return JsonResponse(
                {'code': 1, 'data': '', 'message': '集群%s-主机%s-服务%s-端口%s已经存在！' % (fcluster, fhost, fname, fport)})
        s = Service.objects.create(fhost=fhost, fname=fname, fport=fport, fcluster=fcluster, fdesc=fdesc)
        return JsonResponse({'code': 0, 'data': '', 'message': '服务创建成功！'})

    def delete(self, request):
        fid = request.POST['fid']
        Service.objects.filter(fid=fid).delete()
        return JsonResponse({'code': 0, 'data': '', 'message': '服务删除成功！'})

    def update(self, request):
        fid = request.POST['fid']
        fhost = request.POST['fhost']
        fname = request.POST['fname']
        fport = request.POST['fport']
        fdesc = request.POST['fdesc']
        fcluster = request.POST['fcluster']
        if Service.objects.filter(fhost=fhost, fname=fname, fport=fport, fcluster=fcluster).exclude(fid=fid):
            return JsonResponse(
                {'code': 1, 'data': '', 'message': '集群%s-主机%s-服务%s-端口%s已经存在' % (fcluster, fhost, fname, fport)})
        Service.objects.filter(fid=fid).update(fhost=fhost, fname=fname, fport=fport, fcluster=fcluster, fdesc=fdesc)
        return JsonResponse({'code': 0, 'data': '', 'message': '服务更新成功'})

class StatusView(BaseResView):

    def get(self, request):
        return render(request, 'service/status.html')

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        fhost = request.GET['fhost']
        fname = request.GET['fname']
        fport = request.GET['fport']
        fcluster = request.GET['fcluster']
        data = Service.objects.filter(fcluster__contains=fcluster, fhost__contains=fhost, fname__contains=fname,
                                      fport__contains=fport)[
               (page - 1) * limit: page * limit]
        total = Service.objects.filter(fcluster__contains=fcluster, fhost__contains=fhost, fname__contains=fname,
                                       fport__contains=fport).count()
        result = []
        for i in data:
            result.append({
                'fid': i.fid,
                'fcluster': i.fcluster,
                'fhost': i.fhost,
                'fname': i.fname,
                'fport': i.fport,
                'fdesc': i.fdesc,
                'fcreate_time': str(i.fcreate_time),
                'fstatus': i.fstatus
            })
        return HttpResponse(json.dumps({'total': total, 'rows': result}))

    def graph(self, request):
        fcluster = request.GET['fcluster']
        fservice = request.GET['fservice']
        fhost = request.GET['fhost']
        fport = request.GET['fport']
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 3600  # 默认取1个小时
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        return render(request, 'service/graph.html', locals())



    def query_graph(self, request):
        fhost = request.POST['fhost']
        fservice = request.POST['fservice']
        fport = request.POST['fport']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        start_timestamp = int(time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')))
        end_timestamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))
        f = Falcon()
        counter = '%s/port=%s' % (settings.port_listen_key, fport)
        history_data = f.get_history_data(start_timestamp, end_timestamp, [fhost], [counter], CF='AVERAGE')
        data = history_data[0]['Values']
        #data.reverse()
        time_list = []
        value_list = []
        for i in data:
            time_list.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['timestamp']) ))
            value_list.append(i['value'])

        return JsonResponse({'code':0, 'data':{'time_list':time_list,'value_list':value_list}, 'message':'ok'})



def getport(request):
    host = request.POST['host']
    port_list = [ i.fport for i in Service.objects.filter(fhost=host) ]
    return JsonResponse({'code':0, 'data':{'port_list':port_list}, 'message':'ok'})
