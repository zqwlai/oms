"""oms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt
from django.conf.urls import handler404, handler500
import settings
from django.views.generic.base import RedirectView
from django.views.static import serve
import django.views
import django.views.static
static_serve = login_exempt(django.views.static.serve)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^login$', login_exempt(TemplateView.as_view(template_name="login.html"))),
    url(r'^register$', login_exempt(TemplateView.as_view(template_name="register.html"))),
    url(r'^process_login$', login_exempt(views.process_login)),
    url(r'^process_register$', login_exempt(views.process_register)),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', login_exempt(views.logout)),
    url(r'^user/', include('user_app.urls')),
    url(r'^service/', include('service_app.urls')),
    url(r'^api/', include('service_app.api_urls')),
    url(r'^rbac/', include('rbac.urls')),
    url(r'^alarm/', include('alarm.urls')),
    url(r'^site_static/(?P<path>.*)$',static_serve,{'document_root':settings.STATIC_ROOT,}),

]


handler404 = views.handler_404
handler500  = views.handler_500



