# coding: UTF-8 -*-

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from user_app.models import OmsUser
from oms import settings
import time
import json
from common.falcon import Falcon
import traceback

class FalconBackend(ModelBackend):
    """
    对接falcon的用户认证
    """

    def authenticate(self, username, password):
        try:
            user_model = get_user_model()
            f = Falcon()
            ret = f.login(username, password)
            if not ret.has_key('error'):
                #获取falcon里该用户的信息详情，比如手机号、邮箱地址等，更新到OMS用户表
                userinfo = f.get_userinfo(username)
                if not userinfo.has_key('error'):
                    try:
                        user = user_model._default_manager.get_by_natural_key(username)
                        user.qq = userinfo.get('qq', '')
                        user.cname = userinfo.get('cnname', '')
                        user.phone = userinfo.get('phone', '')
                        user.email = userinfo.get('email', '')
                        user.role = userinfo.get('role', '')
                        user.save()
                    except user_model.DoesNotExist:
                        user = user_model(
                            username=username,
                            cname=userinfo.get('cnname', ''),
                            phone=userinfo.get('phone', ''),
                            email=userinfo.get('email', ''),
                            qq=userinfo.get('qq', ''),
                            is_staff=1,
                            role = userinfo.get('role', '')
                        )
                        user.save()
                    return user
        except Exception, e:
            pass
        return

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return OmsUser.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
