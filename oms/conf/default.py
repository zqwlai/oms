#-*-coding:utf-8-*-
import os

# 项目路径

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*8vp45-y4fzeyvi!%gg_aleg=%th((sq9z8v7&syhbtnd&rve%'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_app',
    'service_app',
    'docker',
    'rbac',
    'alarm'
	
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'common.middleware.LogRecordMiddleware',
    'common.middleware.LoginMiddleware',
    #'common.middleware.RbacMiddleware',  # 权限中间件
)

ROOT_URLCONF = 'oms.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.mysetting',
                'common.context_processors.menu_list'
            ],
        },
    },
]

WSGI_APPLICATION = 'oms.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/



STATIC_URL = '/static/'

STATIC_ROOT=os.path.join(BASE_DIR,"static")


request_log = '/var/logs/oms/request.log'
response_log = '/var/logs/oms/response.log'
log_500 = '/var/logs/oms/500.log'

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


AUTH_USER_MODEL = 'user_app.OmsUser'

AUTHENTICATION_BACKENDS = ('common.backends.FalconBackend' ,'django.contrib.auth.backends.ModelBackend',)
