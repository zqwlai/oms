#-*-coding:utf-8-*-

'''
 每隔12个小时计算每个集群的可用性，为什么是12个小时呢，因为rrd在step为1分钟的情况下会存12个小时的精确数据，会存720个点，在计算这12个小时内的数据时，数据不会失真
'''

import os
import sys
import time 
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DJANGO_SETTINGS_MODULE']='oms.settings'

from common.falcon import Falcon
from common.utils import get_local_ip


from service_app.models import Service
from docker.models import VirtualMachine
from oms import settings


def gen_tags(tags):
    ret = {}
    for i in tags.split(','):
        key = i.split('=')[0]
        value = i.split('=')[1]
        ret[key] = value
    return ret

    

falcon_domain = settings.falcon_domain

falcon_user = 'root'
falcon_sig = settings.falcon_sig

port_listen_key = settings.port_listen_key

end_time = int(time.time()) # 必须要整形
start_time = end_time - 12*60*60
directiry="/api/v1/graph/history"


api_token = '{"name":"' + falcon_user + '", "sig":"' + falcon_sig + '"}'

falcon_header = {
    "Apitoken": api_token,
    #"X-Forwarded-For": "127.0.0.1",
    "Content-Type": "application/json",
    "name": falcon_user,
    "sig": falcon_sig
}

params = {
    'url': falcon_domain + directiry,
    'headers': falcon_header,
    'timeout': 30
}


p = []
ts = int(time.time())

#先统计主机列表


for i in Service.objects.values('fcluster').distinct():
    cluster_name = i['fcluster']
    host_list = []
    port_list = []
    weight_info = {}
    for j in Service.objects.filter(fcluster=i['fcluster']):
        if j.fhost:
            host_list.append(j.fhost)
        if j.fport:
            port_list.append(str(j.fport))
        if j.fhost and j.fport:
            weight_info['%s_%s'%(j.fhost, j.fport)] = j.fweight

    host_list = list(set(host_list))
    port_list = list(set(port_list))

    counter_list = ['listen.port/port=%s,project=oms'%i for i in port_list]
    print host_list

    payload = {
       "step": 60,
       "start_time": start_time,
       "hostnames": host_list,
       "end_time": end_time,
       "counters": counter_list,
       "consol_fun": "AVERAGE"
    }    

    
    params['data'] = json.dumps(payload)

    r = requests.post(**params)
    data = r.json()
    #print data

    weight = 0
    success_count = 0
    total = 0
    for i in data:
        values = i['Values']
        counter = i['counter']
        endpoint = i['endpoint']
        tags = counter.split('/')[1]
        tag_dict = gen_tags(tags)
        port = tag_dict['port']
        if values:
            weight += tag_dict.get('%s_%s'%(endpoint, port), 1)
            success_list = [j['value'] for j in values if j['value'] != 0]
            success_count += weight*len(success_list)
            total += weight*len(values)

    if success_count == 0:
        cluster_available_rate = 100

    else:
        cluster_available_rate = '%.2f'%(float(success_count)/total*100)


    p.append({
        'endpoint': get_local_ip() ,
        'metric': 'cluster.available.percent',
        'timestamp': ts,
        'step': 12*60*60,
        'value': cluster_available_rate,
        'counterType': 'GAUGE',
        'tags': 'clusterName=%s,project=oms'%cluster_name
    }) 



if p:
    r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(p))
    print r.text
            
            
