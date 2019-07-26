#-*-coding:utf-8-*-

import os
import sys
import time 
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DJANGO_SETTINGS_MODULE']='oms.settings'

from common.falcon import Falcon


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

falcon_user = settings.falcon_user
falcon_sig = settings.falcon_sig

port_listen_key = settings.port_listen_key

end_time = int(time.time()) # 必须要整形
start_time = end_time - 70 # 70s 如果本地的服务器时间大于标准时间，可能会取一个未来时间的值，这个当然会取不到，所以取比1分钟稍大的一个值
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

#先统计主机列表

hostname_list = []

for i in Service.objects.values('fhostname').distinct():
    hostname_list.append(i['fhostname'])



for hostname in hostname_list:
    #统计每个主机下有哪些端口号
    counters = []
    for i in Service.objects.filter(fhostname=hostname):
        counters.append('listen.port/port=%s,project=oms'%i.fport)
        
    payload = {
       "step": 60,
       "start_time": start_time,
       "hostnames": [hostname],
       "end_time": end_time,
       "counters": counters,
       "consol_fun": "AVERAGE"
    }    

    
    params['data'] = json.dumps(payload)

    r = requests.post(**params)
    data = r.json()
    print data
    for i in data:
        endpoint = i['endpoint']  
        counter = i['counter'] 
        tags = counter.split('/')[1]
        tag_dict = gen_tags(tags)
        port = tag_dict['port']
        values = i['Values'] 
        status = 0      #0:未知，1:正常，2:异常
        if values:      #如果期间没有收到上报数据，则认为是未知状态
            if values[0]['value'] != None :
                if values[0]['value'] == 1:
                    status = 1
                else:
                    status = 2
        #将状态更新到数据库
        Service.objects.filter(fhostname=endpoint, fport=port).update(fstatus=status,fmodify_time=time.strftime('%Y-%m-%d %H:%M:%S'))


endpoint_list = []

for i in VirtualMachine.objects.all():
    endpoint_list.append('%s/%s'%(i.fmaster, i.fhostname))
payload = {
"step": 60,
"start_time": start_time,
"hostnames": endpoint_list,
"end_time": end_time,
"counters": ["process.status/project=oms"],
"consol_fun": "AVERAGE"
}

params['data'] = json.dumps(payload)
r = requests.post(**params)
data = r.json()
print data
for i in data:
    endpoint = i['endpoint']
    master = endpoint.split('/')[0]
    hostname = endpoint.split('/')[1]
    values = i['Values']
    status = 0  
    if values:
        if values[0]['value'] != None :
            if values[0]['value'] == 1:
                status = 1
            else:
                status = 2
    #将状态更新到数据库
    VirtualMachine.objects.filter(fhostname=hostname, fmaster=master).update(fstatus=status,fmodify_time=time.strftime('%Y-%m-%d %H:%M:%S'))


