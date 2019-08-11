#-*-coding:utf-8-*-
import os

DEBUG = True

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
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}


############   open-falcon相关配置    ########

falcon_sig = 'default-token-used-in-server-side'
falcon_domain = 'http://127.0.0.1:8080'
port_listen_key = 'listen.port'
