from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt



urlpatterns = [
    url(r'^menu$', views.menu_list),
    url(r'^menu/update$', views.update_menu),
    url(r'^menu/data', views.data),
]

urlpatterns += views.RoleView.urls()