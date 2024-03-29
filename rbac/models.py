from django.db import models
from user_app.models import OmsUser
# Create your models here.



class TSysPermission(models.Model):
    fid = models.AutoField(db_column='Fresource_id', primary_key=True)  # Field name made lowercase.
    fparent_id = models.IntegerField(db_column='Fparent_id')  # Field name made lowercase.
    fmenu_icon = models.CharField(db_column='Fmenu_icon', max_length=64)  # Field name made lowercase.
    fresource_name = models.CharField(db_column='Fresource_name', max_length=64)  # Field name made lowercase.
    fresource_url = models.CharField(db_column='Fresource_url', unique=True, max_length=200)  # Field name made lowercase.
    flocal = models.IntegerField(db_column='Flocal')  # Field name made lowercase.
    favailable = models.IntegerField(db_column='Favailable')  # Field name made lowercase.
    fcreate_time = models.DateTimeField(db_column='Fcreate_time', auto_now_add=True)  # Field name made lowercase.
    fmodify_time = models.DateTimeField(db_column='Fmodify_time', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 't_oms_sys_permission'


    def __str__(self):
        return self.fresource_name



class TSysRole(models.Model):
    fid = models.AutoField(db_column='Fid', primary_key=True)  # Field name made lowercase.
    fname = models.CharField(db_column='Fname', max_length=64)
    fcname = models.CharField(db_column='Fcname', max_length=64)
    users = models.ManyToManyField(OmsUser)
    permissions = models.ManyToManyField(TSysPermission)
    fcreate_time = models.DateTimeField(db_column='Fcreate_time', auto_now_add=True)  # Field name made lowercase.
    fmodify_time = models.DateTimeField(db_column='Fmodify_time', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 't_oms_sys_role'


    def __str__(self):
        return self.fname



