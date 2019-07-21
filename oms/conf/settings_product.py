#-*-coding:utf-8-*-
import os

DEBUG = False

###############  数据库配置  ###########

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'oms_db',                      # Or path to database file if using sqlite3.
        'USER': os.getenv('DB_USER', 'root'),                    # Not used with sqlite3.
        'PASSWORD': os.getenv('DB_PASSWORD', '123456'),                  # Not used with sqlite3.
        'HOST': os.getenv('DB_ADDR', '127.0.0.1'),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': os.getenv('DB_PORT', 3306),
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}


############   open-falcon相关配置    ########

falcon_sig = 'default-token-used-in-server-side'
FALCON_PORT=os.getenv('FALCON_PORT', 'tcp://127.0.0.1:8080')
falcon_domain = FALCON_PORT.replace('tcp', 'http')
falcon_user = 'admin'
port_listen_key = 'listen.port'
