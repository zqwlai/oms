#coding: UTF-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class OmsUser(AbstractUser):
    phone = models.IntegerField(default=0)
    class Meta:
        db_table = 'oms_user'
