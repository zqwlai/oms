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
from common.item import items

class ConfView(BaseResView):
    def get(self, request):
        return render(request, 'service/list.html')

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        fhostname = request.GET['fhostname']
        fname = request.GET['fname']
        fport = request.GET['fport']
        fcluster = request.GET['fcluster']
        query_dict = {}
        if fhostname:
            query_dict.update({'fhostname__contains': fhostname})
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
            result.append({
                'fid': i.fid, 'fcluster': i.fcluster, 'fname': i.fname, 'fport': i.fport,
                'fdesc': i.fdesc, 'fcreate_time': str(i.fcreate_time), 'fhostname':i.fhostname,
                'fadmin_user':i.fadmin_user, 'fadmin_password':i.fadmin_password})
        return HttpResponse(json.dumps({'total': total, 'rows': result}))


    def add(self, request):
        fhostname = request.POST['fhostname'].strip()
        fname = request.POST['fname'].strip()
        fport = request.POST['fport'].strip()
        fdesc = request.POST['fdesc']
        fcluster = request.POST['fcluster'].strip()
        fadmin_user = request.POST['fadmin_user'].strip()
        fadmin_password = request.POST['fadmin_password'].strip()
        # 判断服务是否已经存在
        if Service.objects.filter(fhostname=fhostname, fname=fname, fport=fport, fcluster=fcluster):
            return JsonResponse(
                {'code': 1, 'data': '', 'message': '集群%s-主机%s-服务%s-端口%s已经存在！' % (fcluster, fhostname, fname, fport)})
        s = Service.objects.create(
            fhostname=fhostname, fname=fname, fport=fport, fcluster=fcluster, fdesc=fdesc,fadmin_user=fadmin_user,fadmin_password=fadmin_password)
        return JsonResponse({'code': 0, 'data': '', 'message': '服务创建成功！'})

    def delete(self, request):
        fid = request.POST['fid']
        Service.objects.filter(fid=fid).delete()
        return JsonResponse({'code': 0, 'data': '', 'message': '服务删除成功！'})

    def update(self, request):
        fid = request.POST['fid']
        fhostname = request.POST['fhostname'].strip()
        fname = request.POST['fname'].strip()
        fport = request.POST['fport'].strip()
        fdesc = request.POST['fdesc'].strip()
        fcluster = request.POST['fcluster'].strip()
        fadmin_user = request.POST['fadmin_user'].strip()
        fadmin_password = request.POST['fadmin_password'].strip()
        if Service.objects.filter(fhostname=fhostname, fname=fname, fport=fport, fcluster=fcluster).exclude(fid=fid):
            return JsonResponse(
                {'code': 1, 'data': '', 'message': '集群%s-主机%s-服务%s-端口%s已经存在' % (fcluster, fhostname, fname, fport)})
        Service.objects.filter(fid=fid).update(
            fname=fname, fhostname=fhostname, fport=fport, fcluster=fcluster, fdesc=fdesc,fadmin_user=fadmin_user,fadmin_password=fadmin_password)

        return JsonResponse({'code': 0, 'data': '', 'message': '服务更新成功'})


    def get_service_obj(self, request):
        fid = request.POST['fid']
        service_obj = Service.objects.get(fid=fid)
        data = {
            'fid':service_obj.fid,'fhostname':service_obj.fhostname,'fname':service_obj.fname,
            'fport':service_obj.fport,'fcluster':service_obj.fcluster,'fdesc':service_obj.fdesc,'fcreate_time':service_obj.fcreate_time,
            'fadmin_user':service_obj.fadmin_user, 'fadmin_password':service_obj.fadmin_password
        }
        return JsonResponse({'code': 0, 'data': data, 'message': 'ok'})


class StatusView(BaseResView):

    def get(self, request):
        fcluster = request.GET.get('fcluster', '')
        return render(request, 'service/status.html', locals())

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        fhostname = request.GET['fhostname']
        fname = request.GET['fname']
        fport = request.GET['fport']
        fcluster = request.GET['fcluster']
        sort = request.GET.get('sort', 'fcluster')
        sortOrder = request.GET['sortOrder']    #['asc', 'desc']
        if sortOrder == 'asc':
            oder_string = sort
        else:
            oder_string = '-' + sort

        data = Service.objects.filter(fcluster__contains=fcluster, fhostname__contains=fhostname, fname__contains=fname,
                                      fport__contains=fport).order_by(oder_string)[
               (page - 1) * limit: page * limit]
        total = Service.objects.filter(fcluster__contains=fcluster, fhostname__contains=fhostname, fname__contains=fname,
                                       fport__contains=fport).count()
        result = []
        for i in data:
            result.append({
                'fid': i.fid,
                'fcluster': i.fcluster,
                'fhostname':i.fhostname,
                'fname': i.fname,
                'fport': i.fport,
                'fdesc': i.fdesc,
                'fcreate_time': str(i.fcreate_time),
                'fstatus': i.fstatus
            })
        return HttpResponse(json.dumps({'total': total, 'rows': result}))

    def port(self, request):
        fid = request.GET['fid']
        service_obj = Service.objects.get(fid=fid)
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 3600  # 默认取1个小时
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        counter = '%s/port=%s'%(settings.port_listen_key, service_obj.fport)
        return render(request, 'service/port.html', locals())



    def query_graph(self, request):
        fid = request.POST['fid']
        metric = request.POST['metric']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        start_timestamp = int(time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')))
        end_timestamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))
        service_obj = Service.objects.get(fid=fid)
        endpoint = service_obj.fhostname
        #统计该组件对应的counter有哪些
        item_list = items[service_obj.fname][metric]
        counter_list = ['%s/%s=%s'%(i, service_obj.fname, service_obj.fport) for i in item_list]
        #print counter_list
        f = Falcon()
        history_data = f.get_history_data(start_timestamp, end_timestamp, [endpoint], counter_list, CF='AVERAGE')
        #print history_data[0]
        hdata = []
        for i in history_data:
            hdata.append({'name':i['counter'], 'data':[[j['timestamp'], j['value'] ]for j in i['Values']]})

        return JsonResponse({'code':0, 'data':{'hdata':hdata}, 'message':'ok'})


    def performance(self, request):
        try:
            fid = request.GET['fid']
            #获取该服务有哪些counter
            service_obj = Service.objects.get(fid=fid)
            #获取该服务下有哪些聚合的metric
            metric_list = items.get(service_obj.fname, {})
            metric_list = sorted(metric_list.items(), key=lambda x: x[1], reverse=True)
            end_timestamp = int(time.time())
            start_timestamp = end_timestamp - 3600  # 默认取1个小时
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        except:
            print traceback.format_exc()
        return render(request, 'service/performance.html', locals())



def getcomponent(request):  #获取对应主机下所有的组件信息
    hostname = request.POST['hostname']
    Service.objects.filter(fhostname=hostname)
    data = []
    for i in Service.objects.filter(fhostname=hostname):
        data.append({'fname':i.fname, 'fport':i.fport,'fadmin_user':i.fadmin_user,'fadmin_password':i.fadmin_password})
    return JsonResponse({'code':0, 'data':data, 'message':'ok'})