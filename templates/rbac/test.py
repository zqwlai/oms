#! /bin/env python
#-*- coding:utf8 -*
import time
import urllib,urllib2
import json
import commands
import socket
import sys

import fileinput
#port = sys.argv[1]

#endpoint = socket.gethostname()


zk_list= []
for line in fileinput.input():
    zk_list.append(line.strip())
for zk_info in zk_list:
    host,port,endpoint = zk_info.split(',')


    # stat 命令的结果处理
    zookeeper_stat_received = commands.getoutput("echo stat | nc %s %s | grep \"Received:\" | awk '{print $2}'"%(host,port))
    zookeeper_stat_sent = commands.getoutput("echo stat | nc %s %s | grep \"Sent:\" | awk '{print $2}'"%(host,port))
    zookeeper_stat_connections = commands.getoutput("echo stat | nc %s %s |grep \"Connections:\" | awk '{print $2}'"%(host,port))
    zookeeper_stat_outstanding = commands.getoutput("echo stat | nc %s %s |grep \"Outstanding:\" | awk '{print $2}'"%(host,port))
    zookeeper_stat_nodecount = commands.getoutput("echo stat | nc %s %s |grep \"Node count:\" | awk '{print $3}'"%(host,port))


    # wchs 命令的结果处理
    zookeeper_wchs_connections=commands.getoutput("echo wchs | nc %s %s |head -n1 | awk '{print $1}'"%(host,port))
    zookeeper_wchs_watchingpaths = commands.getoutput("echo wchs | nc %s %s |head -n1 | awk '{print $4}'"%(host,port))
    zookeeper_wchs_totalwatches = commands.getoutput("echo wchs | nc %s %s |grep 'Total watches' | awk -F\: '{print $2}'"%(host,port))


    # ruok 命令的结果处理
    zookeeper_ruok = commands.getoutput("echo ruok | nc %s %s |grep 'imok' | wc -l"%(host, port))


    items = [
    {'name': 'zookeeper_stat_received', 'type': 'COUNTER'},
    {'name':'zookeeper_stat_sent', 'type':'COUNTER'},
    {'name': 'zookeeper_stat_connections', 'type': 'GAUGE'},
    {'name': 'zookeeper_stat_outstanding', 'type': 'COUNTER'},
    {'name': 'zookeeper_stat_nodecount', 'type':'GAUGE'},
    {'name': 'zookeeper_wchs_connections', 'type':'GAUGE'},
    {'name': 'zookeeper_wchs_watchingpaths', 'type': 'GAUGE'},
    {'name': 'zookeeper_wchs_totalwatches', 'type': 'GAUGE'},
    {'name': 'zookeeper_ruok', 'type': 'GAUGE'}

    ]


    payload = []


    for item in items:
        payload.append({
        "endpoint": endpoint,
        "metric": item['name'],
        "timestamp": int(time.time()),
        "step": 60,
        "value": locals()[item['name']],
        "counterType": item['type'],
        "tags": "zookeeper=%s"%port
    })


    print json.dumps(payload, indent=2)
    request_url = 'http://127.0.0.1:1988/v1/push'
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=request_url, headers=headers, data=json.dumps(payload))
    response = urllib2.urlopen(request)
    print response.read()
