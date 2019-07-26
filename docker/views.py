#coding: UTF-8 -*-

from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from  docker.models import VirtualMachine
import time
import json
from common.falcon import Falcon
from oms import settings
import traceback
from oms.views import BaseResView
from common.item import items



class StatusView(BaseResView):

    def get(self, request):
        fmaster = request.GET.get('fmaster', '')
        fhostname = request.GET.get('fhostname', '')
        return render(request, 'docker/status.html', locals())

    def data(self, request):
        try:
            limit = int(request.GET['limit'])
            page = int(request.GET['page'])
            fhostname = request.GET['fhostname']
            fmaster = request.GET['fmaster']
            sort = request.GET.get('sort', 'fmaster')
            sortOrder = request.GET['sortOrder']    #['asc', 'desc']
            fstatus = request.GET.get('fstatus', '')
            if sortOrder == 'asc':
                oder_string = sort
            else:
                oder_string = '-' + sort
            query_dict = {
                'fmaster__contains':fmaster,
                'fhostname__contains':fhostname,
            }
            if fstatus:
                query_dict.update({'fstatus':fstatus})

            data = VirtualMachine.objects.filter(**query_dict).order_by(oder_string)[
                   (page - 1) * limit: page * limit]
            total = VirtualMachine.objects.filter(**query_dict).count()
            result = []
            for i in data:
                result.append({
                    'fid': i.fid,
                    'fmaster': i.fmaster,
                    'fhostname':i.fhostname,
                    'fcreate_time': str(i.fcreate_time),
                    'fstatus': i.fstatus
                })
        except:
            print traceback.format_exc()
        return HttpResponse(json.dumps({'total': total, 'rows': result}))

    def process(self, request):
        fid = request.GET['fid']
        container_obj = VirtualMachine.objects.get(fid=fid)
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 3600  # 默认取1个小时
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        counter = 'process.status/project=oms'
        return render(request, 'docker/process.html', locals())


    def query_graph2(self, request):
        fid = request.POST['fid']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        counter = request.POST['counter']
        start_timestamp = int(time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')))
        end_timestamp = int(time.mktime(time.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))
        container_obj = VirtualMachine.objects.get(fid=fid)
        endpoint = container_obj.fmaster + '/' + container_obj.fhostname
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
        container_obj = VirtualMachine.objects.get(fid=fid)
        endpoint = container_obj.fmaster + '/' + container_obj.fhostname
        print endpoint
        #统计该组件对应的大metric有哪些
        all_data = []
        for metric,item_list in items['docker'].items():

            counter_list = [i for i in item_list]
            print counter_list
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
            container_obj = VirtualMachine.objects.get(fid=fid)
            #获取该服务下有哪些聚合的metric
            metric_list = items.get('docker', {})
            metric_list = sorted(metric_list.items(), key=lambda x: x[1], reverse=True)
            metric_list_length = len(metric_list)
            end_timestamp = int(time.time())
            start_timestamp = end_timestamp - 3600  # 默认取1个小时
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_timestamp))
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_timestamp))
        except:
            print traceback.format_exc()
        return render(request, 'docker/performance.html', locals())


