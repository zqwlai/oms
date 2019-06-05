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
from oms import settings



falcon_domain = settings.falcon_domain

falcon_user = settings.falcon_user
falcon_sig = settings.falcon_sig

port_listen_key = settings.port_listen_key

end_time = int(time.time()) # 必须要整形
start_time = end_time - 120 # 2分钟    #如果本地的服务器时间大于标准时间，可能会取一个未来时间的值，这个当然会取不到，所以取2分钟之前的数据
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

#先统计IP列表

ip_list = []

for i in Service.objects.values('Fhost').distinct():
    ip_list.append(i['Fhost'])



for ip in ip_list:
    #统计每个IP下有哪些端口号
    counters = []
    for i in Service.objects.filter(Fhost=ip):
        counters.append('listen.port/port=%s'%i.Fport)
        
    payload = {
       "step": 60,
       "start_time": start_time,
       "hostnames": [ip],
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
        port = counter.split('=')[1]
        values = i['Values'] 
        status = 0
        if values:
            if values[0]['value'] 
                if values[0]['value'] == 1:
                    status = 1
                else:
                    status = 2

        #将状态更新到数据库
        Service.objects.filter(Fhost=endpoint, Fport=port).update(Fstatus=status,Fmodify_time=time.strftime('%Y-%m-%d %H:%M:%S'))


