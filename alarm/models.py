from django.db import models
# Create your models here.



class TConfig(models.Model):
    fid = models.AutoField(db_column='Fid', primary_key=True)  # Field name made lowercase.
    fkey = models.CharField(db_column='Fkey', max_length=64, unique=True)  # Field name made lowercase.
    fvalue = models.TextField(db_column='Fvalue')
    fcreate_time = models.DateTimeField(db_column='Fcreate_time', auto_now_add=True)  # Field name made lowercase.
    fmodify_time = models.DateTimeField(db_column='Fmodify_time', auto_now=True)  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 't_config'

class TMailServer(models.Model):
    fid = models.AutoField(db_column='Fid', primary_key=True)  # Field name made lowercase.
    fhost = models.CharField(db_column='Fhost', max_length=64)  # Field name made lowercase.
    fuser = models.CharField(db_column='Fuser', max_length=64)  # Field name made lowercase.
    fpassword = models.CharField(db_column='Fpassword', max_length=200)  # Field name made lowercase.
    fcreate_time = models.DateTimeField(db_column='Fcreate_time', auto_now_add=True)  # Field name made lowercase.
    fmodify_time = models.DateTimeField(db_column='Fmodify_time', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 't_mail_server'



