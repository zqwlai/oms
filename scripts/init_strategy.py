# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2017/12/15
import json
import time
import requests

user = 'root'
#sig = 'fd3acf4e804d11e986b7005056891887' # 注:sig为数据库uic表中用户对应的sig
#sig = '41cee1bd7e9811e99971080027f300ca'
sig = 'default-token-used-in-server-side'
domain = 'http://127.0.0.1:8080'    # api对应端口为8080
api_token = '{"name":"' + user + '", "sig":"' + sig + '"}'

falcon_header = {
            "Apitoken": api_token,
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/json",
            "name": user,
            "sig": sig
        }


def add_user():
    directiry="/api/v1/user/create"
    params = {
        'url': domain + directiry,
        'headers': falcon_header,
        'timeout': 30
    }

    payload = {
        "name": "root",
        "password": "root",
        "cnname": "root",
        "email": "xx@xx.com",
        "im": "44955834958",
        "phone": "99999999999",
        "qq": "904394234239"
    }
    params['data'] = json.dumps(payload)

    res3 = requests.post(**params)
    data3 = json.loads(res3.text)
    # print('得到指定监控项的历史记录',data3)
    return data3



def get_users():
    directiry="/api/v1/user/users"
    params = {
        'url': domain + directiry,
        'headers': falcon_header,
        'timeout': 30
    }

    payload = {
        
    }

    params['data'] = json.dumps(payload)

    res3 = requests.get(**params)
    data3 = json.loads(res3.text)
    # print('得到指定监控项的历史记录',data3)
    return data3


def add_team(team, users):
    directiry="/api/v1/team"
    params = {
        'url': domain + directiry,
        'headers': falcon_header,
        'timeout': 30
    }

    payload = {
        "team_name": team,
        "resume": team,
        "users": users
    }

    params['data'] = json.dumps(payload)
    res3 = requests.post(**params)
    data3 = json.loads(res3.text)
    # print('得到指定监控项的历史记录',data3)
    print data3
    return data3


def create_expression():
    directiry="/api/v1/expression"
    params = {
        'url': domain + directiry,
        'headers': falcon_header,
        'timeout': 30
    }

    payload = {
      "right_value": "0",
      "priority": 1,
      "pause": 0,
      "op": "==",
      "note": "端口异常",
      "max_step": 3,
      "func": "all(#1)",
      "expression": "each(metric=listen.port project=oms)",
      "action": {
        "url": "",
        "uic": [
          "default"
        ],
        "callback": 0,
        "before_callback_sms": 0,
        "before_callback_mail": 0,
        "after_callback_sms": 0,
        "after_callback_mail": 1
      }

    }

    params['data'] = json.dumps(payload)
    res3 = requests.post(**params)
    data3 = json.loads(res3.text)
    # print('得到指定监控项的历史记录',data3)
    print data3
    return data3

add_user()
users = get_users()

userid = 0
for i in users:
    if i['name'] == 'root':
        userid = i['id']
        
add_team('default', [userid])


create_expression()
