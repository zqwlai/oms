from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt



urlpatterns = [
    url(r'^getComponent$', login_exempt(views.getcomponent)),
    url(r'^container/list', login_exempt(views.getContainer)),
    url(r'^container/add', login_exempt(views.addContainer)),
    url(r'^query_cluster_status$', login_exempt(views.query_cluster_status)),
    url(r'^query_service_top', login_exempt(views.query_service_top))
]
