from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt



urlpatterns = [
    url(r'^conf$', views.service_list),
    url(r'^conf/data$', views.query_service),
    url(r'^conf/add$', views.add_service),
    url(r'^conf/delete', views.delete_service),
    url(r'^conf/update', views.update),
    url(r'^status$', views.status),
    url(r'^status/data', views.query_status),
    url(r'^status/graph', views.graph),
    url(r'^status/query_graph', views.query_graph),

]
