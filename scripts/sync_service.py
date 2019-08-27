#-*-coding:utf-8-*-

import sys,os
import time
import requests
import json
import traceback
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DJANGO_SETTINGS_MODULE']='oms.settings'
from common.sql_connect import Mysql
from kazoo.client import KazooClient
from service_app.models import Service


def add(cluster, service, host, port, admin_user='', admin_password=''):
    if Service.objects.filter(fcluster=cluster, fhost=host, fport=port ):
        if admin_user or admin_password:
            Service.objects.filter(fcluster=cluster, fhost=fhost, fport=port ).update(fadmin_user=admin_user, fadmin_password=admin_password)
    else:
        Service.objects.create(fcluster=cluster, fname=service, fhost=host, fport=port, fadmin_user=admin_user, fadmin_password=admin_password)



s = Mysql('172.18.3.51', 3601, 'crp_user', 'crpkingdee', 'newmc_rd_mcdb')


sql = "select fnumber,fzkurl,fzkrootpath, fenable from t_mc_environment"

for i in s.query(sql):
    if i['fzkrootpath']:
        print i['fnumber'], i['fzkurl'], i['fzkrootpath']    #biz-baseline-v15-smoke 172.18.2.142:2186 /
        if i['fzkurl'] and i['fenable']: 
            zk = KazooClient(hosts = i['fzkurl'])
            try:
                zk.start(timeout=1)
                node = '%s%s/config/common/var'%(i['fzkrootpath'], i['fnumber'])
                if zk.exists(node):
                    if zk.exists('%s/mq.server.port'%node):
                        service = 'rabbitmq'
                        port = zk.get('%s/mq.server.port'%node)[0]
                        host = zk.get('%s/mq.server.ip'%node)[0]
                        admin_user = zk.get('%s/mq.server.user'%node)[0]
                        admin_password = zk.get('%s/mq.server.password'%node)[0]
                        add(i['fnumber'], service, host, port, admin_user, admin_password)
                    if zk.exists('%s/redis.serversForCache.ip_port'%node):
                        ip_port = zk.get('%s/redis.serversForCache.ip_port'%node)[0]
                        service = 'redis'
                        if ip_port:
                            host = ip_port.split(':')[0]
                            port = ip_port.split(':')[1]
                            add(i['fnumber'], service, host, port)

                    if zk.exists('%s/redis.serversForSession.ip_port'%node):
                        ip_port = zk.get('%s/redis.serversForSession.ip_port'%node)[0]
                        service = 'redis'
                        if ip_port:
                            host = ip_port.split(':')[0]
                            port = ip_port.split(':')[1]
                            add(i['fnumber'], service, host, port)
                         
                    if zk.exists('%s/log.es.ip_port'%node):
                        service = 'elasticsearch'
                        ip_port = zk.get('%s/log.es.ip_port'%node)[0]
                        if ip_port:
                            host = ip_port.split(':')[0]
                            port = ip_port.split(':')[1]
                            add(i['fnumber'], service, host, port)

                    if zk.exists('%s/dubbo.zookeeper.ip_port'%node):
                        service = 'zookeeper'
                        ip_port = zk.get('%s/dubbo.zookeeper.ip_port'%node)[0]
                        if ip_port:
                            host = ip_port.split(':')[0]
                            port = ip_port.split(':')[1]
                            add(i['fnumber'], service, host, port)

                    if zk.exists('%s/Schedule.zk.server.ip_port'%node):
                        service = 'zookeeper'
                        ip_port = zk.get('%s/Schedule.zk.server.ip_port'%node)[0]
                        if ip_port:
                            host = ip_port.split(':')[0]
                            port = ip_port.split(':')[1]
                            add(i['fnumber'], service, host, port)

                    if zk.exists('%s/IDService.store.zookeeper.ip_port'%node):
                        service = 'zookeeper'
                        ip_port = zk.get('%s/IDService.store.zookeeper.ip_port'%node)[0]
                        if ip_port:
                            host = ip_port.split(':')[0]
                            port = ip_port.split(':')[1]
                            add(i['fnumber'], service, host, port)                    

                       
            except Exception,e:
                print traceback.format_exc()



