from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt



urlpatterns = [
    url(r'^profile', TemplateView.as_view(template_name="profile.html")),
    url(r'^update_profile', views.update_profile),
    url(r'^update_password', views.update_password),
]


