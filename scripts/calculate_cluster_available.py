#-*-coding:utf-8-*-

'''
统计前一天的各集群可用率
'''

import os
import sys
import time, datetime 
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DJANGO_SETTINGS_MODULE']='oms.settings'

from common.falcon import Falcon
from common.utils import get_local_ip
from common.calc import get_cluster_available

from service_app.models import Service


a = datetime.datetime.now()
b = a+datetime.timedelta(-1)
yesterday = b.strftime("%Y-%m-%d")


ts = int(time.time())
#先统计主机列表
p = []

for i in Service.objects.values('fcluster').distinct():
    cluster_name = i['fcluster']
    value = get_cluster_available(cluster_name, yesterday)    


    p.append({
        'endpoint': get_local_ip() ,
        'metric': 'cluster.available.percent',
        'timestamp': ts,
        'step': 24*60*60,
        'value': value,
        'counterType': 'GAUGE',
        'tags': 'clusterName=%s,project=oms'%cluster_name
    }) 


if p:
    print json.dumps(p)
    r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(p))
    print r.text
            
            
