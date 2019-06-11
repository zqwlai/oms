from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt



urlpatterns = []
urlpatterns += views.ConfView.urls()
urlpatterns += views.StatusView.urls()
