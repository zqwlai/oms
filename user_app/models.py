#coding: UTF-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class OmsUser(AbstractUser):
    cname = models.CharField(db_column='cname', max_length=20)
    phone = models.CharField(default='',max_length=20)
    class Meta:
        db_table = 'oms_user'


