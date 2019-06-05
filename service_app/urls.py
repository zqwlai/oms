from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt



urlpatterns = [
    url(r'^list$', views.service_list),
    url(r'^query$', views.query_service),
    url(r'^add$', views.add_service),
    url(r'^delete', views.delete_service),
    url(r'^status', views.status),
    url(r'^query_status', views.query_status),
    url(r'^graph', views.graph),
    url(r'^query_graph', views.query_graph),
    url(r'^update', views.update),
]
