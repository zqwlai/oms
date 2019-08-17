#coding: UTF-8 -*-
import json
import time
import requests
import urllib
from oms import settings
from django.http import JsonResponse

def FalconResponse(obj):
    if isinstance(obj, dict):
        if obj.has_key('error'):
            return JsonResponse({'code1':1, 'data':'', 'message':obj['error']})
        return JsonResponse({'code':0, 'data':obj, 'message': 'ok'})
    return JsonResponse({'code':1, 'data':'', 'message': obj})

class Falcon(object):
    def __init__(self, user='root'):
        self.domain = settings.falcon_domain
        self.sig = settings.falcon_sig
        self.user = user
        self.api_token = '{"name":"' + self.user + '", "sig":"' + self.sig + '"}'
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
        response = requests.post(**params)
        return response.json()


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
        response = requests.post(**params)
        return response.json()


    def login(self, username, password):
        '''
        {u'admin': False, u'sig': u'56362913b75c11e9be14005056891887', u'name': u'admin'}
        '''
        directory = '/api/v1/user/login'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'name':username, 'password':password})
        response = requests.post(**params)
        return response.json()


    def get_userinfo(self, username):
        directory = '/api/v1/user/name/%s'%username
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def register(self, username, password, cname, email):
        directory = '/api/v1/user/create'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'name':username, 'password':password, 'email':email, 'cnname':cname})
        response = requests.post(**params)
        print response.text
        return response.json()

    def update_user(self, cnname, email, phone, qq):
        directory = '/api/v1/user/update'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'cnname':cnname, 'email':email, 'phone':phone, 'qq':qq})
        response = requests.put(**params)
        print response.text
        return response.json()

    def query_team(self, q=''):
        if not q:
            q = '.+'
        data = {'q': q}
        data = urllib.urlencode(data)
        directory = '/api/v1/team?%s'%data
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_user_list(self):
        directory = '/api/v1/user/users'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_team_info_by_id(self, id):
        directory = '/api/v1/team/t/%s'%id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def create_team(self, name, resume, users):
        directory = '/api/v1/team'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'team_name':name, 'resume':resume, 'users':users})
        response = requests.post(**params)
        return response.json()

    def update_team(self, id, name, resume, users):
        directory = '/api/v1/team'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'team_id': id, 'name': name, 'resume': resume, 'users': users})
        response = requests.put(**params)
        return response.json()

    def delete_team(self, id):
        directory = '/api/v1/team/%s'%id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.delete(**params)
        return response.json()

    def get_endpoint_list(self, q):
        if not q:
            q = '.+'
        data = {'q': q}
        data = urllib.urlencode(data)
        directory = '/api/v1/graph/endpoint?%s'%data
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_hostgroup_list(self, q):
        if not q:
            q = '.+'
        data = {'q': q}
        data = urllib.urlencode(data)
        directory = '/api/v1/hostgroup?%s'%data
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_templates_of_hostgroup(self, groupid):
        directory = '/api/v1/hostgroup/%s/template' %(groupid)
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_all_template_list(self, q=''):
        if not q:
            q = '.+'
        data = {'q': q}
        data = urllib.urlencode(data)
        directory = '/api/v1/template?%s'%data
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_hostgroups_of_template(self, template_id):
        directory = '/api/v1/template/%s/hostgroup'%template_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_template_info(self, template_id):
        directory = '/api/v1/template/%s'%template_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_all_hostgroup_list(self):
        directory = '/api/v1/hostgroup'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_strategy_info(self, strategy_id):
        directory = '/api/v1/strategy/%s'%strategy_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()


    def update_template(self, template_id, parent_id , name):
        directory = '/api/v1/template'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'tpl_id':template_id, 'parent_id':parent_id, 'name':name})
        response = requests.put(**params)
        return response.json()


    def bindTemplate2HostGroup(self, template_id, hostgroup_id):
        directory = '/api/v1/hostgroup/template'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'tpl_id': template_id, 'grp_id':hostgroup_id})
        response = requests.post(**params)
        return response.json()


    def unbindTemplate2HostGroup(self, template_id, hostgroup_id):
        directory = '/api/v1/hostgroup/template'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({'tpl_id': template_id, 'grp_id':hostgroup_id})
        response = requests.put(**params)
        return response.json()

    def update_strategy(self, strategy_id=0 ,metric='', tags='', max_step=0, priority=0, note='', func='', op='==', right_value=0, run_begin='', run_end=''):
        directory = '/api/v1/strategy'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'id':int(strategy_id),
            'metric':metric,
            'tags':tags,
            'max_step':int(max_step),
            'priority':int(priority),
            'note': note,
            'func': func,
            'op': op,
            'right_value': right_value,
            'run_begin': run_begin,
            'run_end': run_end
        })
        response = requests.put(**params)
        return response.json()


    def create_strategy(self, template_id=0, metric='', tags='', max_step=0, priority=0, note='', func='', op='==', right_value=0, run_begin='', run_end=''):
        directory = '/api/v1/strategy'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'tpl_id':int(template_id),
            'metric':metric,
            'tags':tags,
            'max_step':int(max_step),
            'priority':int(priority),
            'note': note,
            'func': func,
            'op': op,
            'right_value': right_value,
            'run_begin': run_begin,
            'run_end': run_end
        })
        response = requests.post(**params)
        return response.json()


    def  create_action(self, template_id, callback_url='', callback=0, uic='',
        before_callback_sms=0, before_callback_mail=0, after_callback_sms=0, after_callback_mail=0):
        directory = '/api/v1/template/action'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'tpl_id': int(template_id),
            'uic': uic,
            'callback': int(callback),
            'url': callback_url,
            'before_callback_sms': int(before_callback_sms),
            'before_callback_mail': int(before_callback_mail),
            'after_callback_sms': int(after_callback_sms),
            'after_callback_mail': int(after_callback_mail)
        })
        response = requests.post(**params)
        return response.json()


    def  update_action(self, action_id, callback_url='', callback=0, uic='',
        before_callback_sms=0, before_callback_mail=0, after_callback_sms=0, after_callback_mail=0):
        directory = '/api/v1/template/action'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        print uic
        params['data'] = json.dumps({
            'id': int(action_id),
            'uic': uic,
            'callback': int(callback),
            'url': callback_url,
            'before_callback_sms': int(before_callback_sms),
            'before_callback_mail': int(before_callback_mail),
            'after_callback_sms': int(after_callback_sms),
            'after_callback_mail': int(after_callback_mail)
        })
        response = requests.put(**params)
        print response.text
        return response.json()

    def create_template(self, template_name):
        directory = '/api/v1/template'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'name': template_name,
            'parent_id': 0
        })
        response = requests.post(**params)
        return response.json()

    def get_all_expression_list(self):
        directory = '/api/v1/expression'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()

    def get_expression_info_by_id(self, expreesion_id):
        directory = '/api/v1/expression/%s'%expreesion_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        return response.json()


    def create_expression(self, right_value=0, priority=0, op='==', note='', max_step=0, func='', expression='', action={}):
        directory = '/api/v1/expression/'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        action['callback'] = int(action.get('callback', 0))
        action['before_callback_sms'] = int(action.get('before_callback_sms', 0))
        action['before_callback_mail'] = int(action.get('before_callback_mail', 0))
        action['after_callback_sms'] = int(action.get('after_callback_sms', 0))
        action['after_callback_mail'] = int(action.get('after_callback_mail', 0))
        params['data'] = json.dumps({
            'right_value': int(right_value),
            'priority': int(priority),
            'op': op,
            'note': note,
            'max_step': int(max_step),
            'func': func,
            'expression': expression,
            'action':action
        })
        response = requests.post(**params)
        return response.json()


    def update_expression(self, id=0, right_value=0, priority=0, op='==', note='', max_step=0, func='', expression='', action={}):
        directory = '/api/v1/expression/'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        action['callback'] = int(action.get('callback', 0))
        action['before_callback_sms'] = int(action.get('before_callback_sms', 0))
        action['before_callback_mail'] = int(action.get('before_callback_mail', 0))
        action['after_callback_sms'] = int(action.get('after_callback_sms', 0))
        action['after_callback_mail'] = int(action.get('after_callback_mail', 0))
        params['data'] = json.dumps({
            'id': int(id),
            'right_value': right_value,
            'priority': int(priority),
            'op': op,
            'note': note,
            'max_step': int(max_step),
            'func': func,
            'expression': expression,
            'action':action
        })
        response = requests.put(**params)
        return response.json()

    def delete_expression(self, id):
        directory = '/api/v1/expression/%s'%id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.delete(**params)
        return response.json()


    def delete_hostgroup(self, id):
        directory = '/api/v1/hostgroup/%s'%id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.delete(**params)
        return response.json()

    def update_hostgroup(self, hostgroup_id, name):
        directory = '/api/v1/hostgroup'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'id': hostgroup_id,
            'grp_name': name
        })
        response = requests.put(**params)
        print response.text

        return response.json()


    def create_hostgroup(self, name):
        directory = '/api/v1/hostgroup'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'name': name
        })
        response = requests.post(**params)
        print response.text

        return response.json()


    def get_hostgroup_info_by_id(self, id):
        directory = '/api/v1/hostgroup/%s'%id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        print response.text

        return response.json()

    def host_hostgroups(self, host_id):
        directory = '/api/v1/host/%s/hostgroup' % host_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        print response.text

        return response.json()


    def host_templates(self, host_id):
        directory = '/api/v1/host/%s/template' % host_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        print response.text

        return response.json()

    def host_hostgroups(self, host_id):
        directory = '/api/v1/host/%s/hostgroup' % host_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.get(**params)
        print response.text

        return response.json()

    def unbindHost2HostGroup(self, host_id, hostgroup_id):
        directory = '/api/v1/hostgroup/host'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'host_id': host_id,
            'hostgroup_id': hostgroup_id
        })
        response = requests.put(**params)
        print response.text

        return response.json()


    def addHost2HhostGroup(self, hostgroup_id, hostname_list):
        directory = '/api/v1/hostgroup/host'
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        params['data'] = json.dumps({
            'hosts': hostname_list,
            'hostgroup_id': hostgroup_id
        })
        response = requests.post(**params)
        print response.text

        return response.json()


    def delete_template(self, template_id):
        directory = '/api/v1/template/%s'%template_id
        params = {
            'url': self.domain + directory,
            'headers': self.falcon_header,
            'timeout': 30
        }
        response = requests.delete(**params)
        print response.text

        return response.json()
