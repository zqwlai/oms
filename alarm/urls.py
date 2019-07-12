from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt
from django.views.generic.base import RedirectView



urlpatterns = [
    url(r'^sms', login_exempt(views.sms)),

]