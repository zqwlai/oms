#coding: UTF-8 -*-
import json
import time
import requests
from oms import settings

class Falcon(object):
    def __init__(self):
        self.domain = settings.falcon_domain
        self.sig = settings.falcon_sig
        self.user = settings.falcon_user
        self.api_token = '{"name":"' + settings.falcon_user + '", "sig":"' + self.sig + '"}'
        self.falcon_header = {
            "Apitoken": self.api_token,
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/json",
            "name": self.user,
            "sig": self.sig
        }


    def get_history_data(self, start_time, end_time, endpoints, counters, step=60, CF='AVERAGE'):

        directory = '/api/v1/graph/history'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }

        payload = {
            "step": step,
            "start_time": start_time,
            "hostnames": endpoints,
            "end_time": end_time,
            "counters": counters,
            "consol_fun": CF
        }
        print start_time, end_time
        params['data'] = json.dumps(payload)
        r = requests.post(**params)
        return r.json()


    def get_endpoints(self, q):
        directory = '/api/v1/graph/endpoint?q=%s&limit=10000'%q
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        r = requests.get(**params)
        return r.json()


    def get_counters(self, endpoint_id, q='', metricQuery=''):
        directory = '/api/v1/graph/endpoint_counter?eid=%s&q=%slimit=10000&metricQuery=%s' %(endpoint_id, q, metricQuery)
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        r = requests.get(**params)
        return r.json()



    def get_eventcase(self, endpoints='', metrics='', startTime='', endTime='', priority='', Status=''):
        directory = '/api/v1/alarm/eventcases'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        data = {}
        if endpoints:
            data['endpoints'] = endpoints
        if metrics:
            data['metrics'] = metrics
        if  startTime:
            data['startTime'] = startTime
        if  endTime:
            data['endTime'] = endTime
        if  priority:
            data['priority'] = priority
        if   Status:
            data['Status'] = Status
        params['data'] = json.dumps(data)
        rsponse = requests.post(**params)
        ret = json.loads(rsponse.text)
        return ret


    def get_events(self, event_id='', startTime='', endTime=''):
        directory = '/api/v1/alarm/events'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        data = {}
        if event_id:
            data['event_id'] = event_id
        if startTime:
            data['startTime'] = startTime
        if  endTime:
            data['endTime'] = endTime

        params['data'] = json.dumps(data)
        rsponse = requests.post(**params)
        ret = json.loads(rsponse.text)
        return ret