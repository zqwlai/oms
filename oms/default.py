#-*-coding:utf-8-*-
import settings
import os

request_log = '/var/logs/oms/request.log'
response_log = '/var/log/oms/response.log'
log_500 = '/var/log/oms/500.log'

if not os.path.isdir(os.path.dirname(request_log)):
    os.makedirs(os.path.dirname(request_log))

if not os.path.isdir(os.path.dirname(response_log)):
    os.makedirs(os.path.dirname(response_log))

if not os.path.isdir(os.path.dirname(request_log)):
    os.makedirs(os.path.dirname(request_log))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }, # 针对 DEBUG = True 的情况
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s: %(message)s'
        }, # 对日志信息进行格式化，每个字段对应了日志格式中的一个字段，更多字段参考官网文档，我认为这些字段比较合适，输出类似于下面的内容
        # INFO 2016-09-03 16:25:20,067 /home/ubuntu/mysite/views.py views.py views get 29: some info...
    },
    'handlers': {
        'request': {
            'level': 'INFO',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'formatter':'standard',
            'filename': request_log,
            'maxBytes': 800*1024*1024,
            'mode': 'a',
            'backupCount': 30,
            'encoding':'utf-8'
        },
        'response': {
            'level': 'INFO',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'formatter':'standard',
            'filename': response_log,
            'maxBytes': 800*1024*1024,
            'mode': 'a',
            'backupCount': 30,
            'encoding':'utf-8'
        },
        '500': {
            'level': 'INFO',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'formatter':'standard',
            'filename': log_500,
            'maxBytes': 800*1024*1024,
            'mode': 'a',
            'backupCount': 30,
            'encoding':'utf-8'
        },
    },
    'loggers': {
        'request': {
            'handlers' :['request'],    #请求日志
            'level':'INFO',
            'propagate': True # 是否继承父类的log信息
        }, # handlers 来自于上面的 handlers 定义的内容
        'response': {
            'handlers': ['response'],    #响应日志
            'level': 'INFO',
            'propagate': True,
        },
        '500': {
            'handlers' :['500'],    #请求日志
            'level':'INFO',
            'propagate': True # 是否继承父类的log信息
        }, # handlers 来自于上面的 handlers 定义的内容
    }
}
