#coding:utf-8

from service_app.models import Service
from common.falcon import Falcon
from oms import settings
from common.utils import gen_tags
import time

def get_cluster_available(cluster, c_date):  #获取某一天某个集群的可用率
    start_ts = int(time.mktime(time.strptime(c_date, '%Y-%m-%d')))
    end_ts = start_ts + 86400
    host_list = []
    port_list = []
    weight_info = {}
    for j in Service.objects.filter(fcluster=cluster):

        if j.fhost:
            host_list.append(j.fhost)
        if j.fport:
            port_list.append(str(j.fport))
        if j.fhost and j.fport:
            weight_info['%s_%s' % (j.fhost, j.fport)] = j.fweight
    host_list = list(set(host_list))
    port_list = list(set(port_list))
    counter_list = ['listen.port/port=%s,project=oms' % i for i in port_list]
    f = Falcon()
    data = f.get_history_data(start_ts, end_ts, host_list, counter_list, step=60)
    #print data
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
            weight = weight_info.get('%s_%s' % (endpoint, port), 1)
            success_list = [j['value'] for j in values if j['value'] != 0]
            success_count += weight * len(success_list)
            total += weight * len(values)

    if success_count == 0:
        cluster_available_rate = 100

    else:
        cluster_available_rate = float('%.2f' % (float(success_count) / total * 100))

    return cluster_available_rate