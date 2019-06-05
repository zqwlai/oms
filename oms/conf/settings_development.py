#-*-coding:utf-8-*-
import os

DEBUG = True

if not DEBUG:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

###############  数据库配置  ###########

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'oms_db',                      # Or path to database file if using sqlite3.
        'USER': 'oms',                      # Not used with sqlite3.
        'PASSWORD': 'oms',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',
    }
}


############   open-falcon相关配置    ########

falcon_sig = 'fd3acf4e804d11e986b7005056891887'
falcon_domain = 'http://172.18.7.14:8080'
falcon_user = 'admin'
port_listen_key = 'listen.port'
