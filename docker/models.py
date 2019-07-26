from django.db import models


class VirtualMachine(models.Model):
    fid = models.AutoField(db_column='Fid', primary_key=True)  # Field name made lowercase.
    fhostname = models.CharField(db_column='Fhostname', max_length=100)
    fip = models.CharField(db_column='Fip', max_length=15)
    fmaster =  models.CharField(db_column='Fmaster', max_length=100)
    fstatus = models.IntegerField(db_column='Fstatus', max_length=1, default=0)
    fversion = models.CharField(db_column='Fversion', max_length=20)  # Field name made lowercase.
    fcreate_time = models.DateTimeField(db_column='Fcreate_time', auto_now_add=True)  # Field name made lowercase.
    fmodify_time = models.DateTimeField(db_column='Fmodify_time', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 't_virtual_machine'

    def __unicode__(self):
        return self.fhostname
