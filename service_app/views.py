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
        service_list = items.keys()
        service_list.remove('docker')
        return render(request, 'service/list.html', locals())


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
            query_dict.update({'fcluster__contains': fcluster})

        data = Service.objects.filter(**query_dict)[(page - 1) * limit: page * limit]
        total = Service.objects.filter(**query_dict).count()
        result = []
        for i in data:
            result.append({
                'fid': i.fid, 'fcluster': i.fcluster, 'fname': i.fname, 'fport': i.fport,
                'fdesc': i.fdesc, 'fcreate_time': str(i.fcreate_time), 'fhostname':i.fhostname, 'fhost': i.fhost,
                'fadmin_user':i.fadmin_user, 'fadmin_password':i.fadmin_password})
            print (i.fcreate_time)
        return HttpResponse(json.dumps({'total': total, 'rows': result}))



    def add(self, request):
        fhost = request.POST['fhost'].strip()
        fname = request.POST['fname'].strip()
        fport = request.POST['fport'].strip()
        fdesc = request.POST['fdesc']
        fcluster = request.POST['fcluster'].strip()
        fadmin_user = request.POST['fadmin_user'].strip()
        fadmin_password = request.POST['fadmin_password'].strip()
        # 判断服务是否已经存在
        if Service.objects.filter(fhost=fhost, fname=fname, fport=fport, fcluster=fcluster):
            return JsonResponse(
                {'code': 1, 'data': '', 'message': '集群%s-主机%s-服务%s-端口%s已经存在！' % (fcluster, fhost, fname, fport)})
        s = Service.objects.create(
            fhost=fhost, fname=fname, fport=fport, fcluster=fcluster, fdesc=fdesc,fadmin_user=fadmin_user,fadmin_password=fadmin_password)
        return JsonResponse({'code': 0, 'data': '', 'message': '服务创建成功！'})

    def delete(self, request):
        fid = request.POST['fid']
        Service.objects.filter(fid=fid).delete()
        return JsonResponse({'code': 0, 'data': '', 'message': '服务删除成功！'})

    def update(self, request):
        fid = request.POST['fid']
        fhost = request.POST['fhost'].strip()
        fname = request.POST['fname'].strip()
        fport = request.POST['fport'].strip()
        fdesc = request.POST['fdesc'].strip()
        fcluster = request.POST['fcluster'].strip()
        fadmin_user = request.POST['fadmin_user'].strip()
        fadmin_password = request.POST['fadmin_password'].strip()
        if Service.objects.filter(fhost=fhost, fname=fname, fport=fport, fcluster=fcluster).exclude(fid=fid):
            return JsonResponse(
                {'code': 1, 'data': '', 'message': '集群%s-主机%s-服务%s-端口%s已经存在' % (fcluster, fhost, fname, fport)})
        Service.objects.filter(fid=fid).update(
            fname=fname, fhost=fhost, fport=fport, fcluster=fcluster, fdesc=fdesc,fadmin_user=fadmin_user,fadmin_password=fadmin_password)
        return JsonResponse({'code': 0, 'data': '', 'message': '服务更新成功'})


    def get_service_obj(self, request):
        fid = request.POST['fid']
        service_obj = Service.objects.get(fid=fid)
        data = {
            'fid':service_obj.fid,'fhostname':service_obj.fhostname,'fname':service_obj.fname,
            'fhost': service_obj.fhost,
            'fport':service_obj.fport,'fcluster':service_obj.fcluster,'fdesc':service_obj.fdesc,'fcreate_time':service_obj.fcreate_time,
            'fadmin_user':service_obj.fadmin_user, 'fadmin_password':service_obj.fadmin_password
        }
        return JsonResponse({'code': 0, 'data': data, 'message': 'ok'})


class StatusView(BaseResView):

    def get(self, request):
        fcluster = request.GET.get('fcluster', '')
        fstatus = request.GET.get('fstatus', '')
        return render(request, 'service/status.html', locals())

    def data(self, request):
        limit = int(request.GET['limit'])
        page = int(request.GET['page'])
        fhost = request.GET['fhost']
        fname = request.GET['fname']
        fport = request.GET['fport']
        fcluster = request.GET['fcluster']
        sort = request.GET.get('sort', 'fcluster')
        sortOrder = request.GET['sortOrder']    #['asc', 'desc']
        fstatus = request.GET.get('fstatus', '')
        if sortOrder == 'asc':
            oder_string = sort
        else:
            oder_string = '-' + sort
        query_dict = {
            'fcluster__contains':fcluster,
            'fhost__contains':fhost,
            'fname__contains':fname,
            'fport__contains': fport
        }
        if fstatus:
            query_dict.update({'fstatus':fstatus})

        data = Service.objects.filter(**query_dict).order_by(oder_string)[
               (page - 1) * limit: page * limit]
        total = Service.objects.filter(**query_dict).count()
        result = []
        for i in data:
            result.append({
                'fid': i.fid,
                'fcluster': i.fcluster,
                'fhost': i.fhost,
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
        counter = '%s/port=%s,project=oms'%(settings.port_listen_key, service_obj.fport)
        return render(request, 'service/port.html', locals())


    def query_graph2(self, request):
        fid = request.POST['fid']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        counter = request.POST['counter']
        start_timestamp = int(time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')))
        end_timestamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))
        service_obj = Service.objects.get(fid=fid)
        endpoint = service_obj.fhost
        f = Falcon()
        history_data = f.get_history_data(start_timestamp, end_timestamp, [endpoint], [counter], CF='AVERAGE')
        # print history_data[0]
        hdata = []
        for i in history_data:
            hdata.append({'name': i['endpoint'], 'data': [[j['timestamp'], j['value']] for j in i['Values']]})
        return JsonResponse({'code': 0, 'data': {'hdata': hdata}, 'message': 'ok'})


    def query_graph(self, request):
        fid = request.POST['fid']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        start_timestamp = int(time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')))
        end_timestamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))
        service_obj = Service.objects.get(fid=fid)
        endpoint = service_obj.fhost
        #统计该组件对应的大metric有哪些
        all_data = []
        for metric,item_list in items[service_obj.fname].items():


            counter_list = ['%s/%sport=%s'%(i, service_obj.fname, service_obj.fport) for i in item_list]
            #print counter_list
            f = Falcon()
            history_data = f.get_history_data(start_timestamp, end_timestamp, [endpoint], counter_list, CF='AVERAGE')
            #print history_data[0]
            hdata = []
            for i in history_data:
                hdata.append({'name':i['counter'], 'data':[[j['timestamp'], j['value'] ]for j in i['Values']]})
            all_data.append({'metric':metric, 'hdata':hdata})

        return JsonResponse({'code':0, 'data':{'all_data':all_data}, 'message':'ok'})


    def performance(self, request):
        try:
            fid = request.GET['fid']
            #获取该服务有哪些counter
            service_obj = Service.objects.get(fid=fid)
            #获取该服务下有哪些聚合的metric
            metric_list = items.get(service_obj.fname, {})
            metric_list = sorted(metric_list.items(), key=lambda x: x[1], reverse=True)
            metric_list_length = len(metric_list)
            end_timestamp = int(time.time())
            start_timestamp = end_timestamp - 3600  # 默认取1个小时
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        except:
            print traceback.format_exc()
        return render(request, 'service/performance.html', locals())



