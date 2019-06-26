from django.db import models

# Create your models here.

'''
class Cluster(models.Model):
    Fid = models.AutoField(db_column='Fid', primary_key=True)  # Field name made lowercase.
    Fname = models.CharField(db_column='Fname', max_length=100, default='')
    Fversion = models.CharField(db_column='Fversion', max_length=20)  # Field name made lowercase.
    Fcreate_time = models.DateTimeField(db_column='Fcreate_time', auto_now_add=True)  # Field name made lowercase.
    Fmodify_time = models.DateTimeField(db_column='Fmodify_time', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 't_oms_cluster'

    def __unicode__(self):
        return self.Fname
'''



class Service(models.Model):
    fid = models.AutoField(db_column='Fid', primary_key=True)  # Field name made lowercase.
    #clusters = models.ManyToManyField(Cluster)  
    fcluster = models.CharField(db_column='Fcluster', max_length=100, default='')
    fhost = models.CharField(db_column='Fhost', max_length=15)  # Field name made lowercase.
    fhostname = models.CharField(db_column='Fhostname', max_length=100)
    fname = models.CharField(db_column='Fname', max_length=100)
    fport = models.IntegerField(db_column='Fport', max_length=5, default=0)
    fdesc = models.CharField(db_column='Fdesc', max_length=100)  # Field name made lowercase.
    fstatus = models.IntegerField(db_column='Fstatus', max_length=1, default=0) 
    fversion = models.CharField(db_column='Fversion', max_length=20)  # Field name made lowercase.
    fcreate_time = models.DateTimeField(db_column='Fcreate_time', auto_now_add=True)  # Field name made lowercase.
    fmodify_time = models.DateTimeField(db_column='Fmodify_time', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 't_oms_service'

    def __unicode__(self):
        return self.fname
