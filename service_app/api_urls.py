from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt



urlpatterns = [
    url(r'^getComponent$', login_exempt(views.getcomponent))
]
