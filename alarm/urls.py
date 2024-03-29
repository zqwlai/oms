from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
from common.decorators import  login_exempt

urlpatterns = []

urlpatterns += views.EventcaseView.urls()
urlpatterns += views.SenderView.urls()
urlpatterns += views.HostGroupView.urls()
urlpatterns += views.TemplateView.urls()
urlpatterns += views.ExpressionView.urls()
