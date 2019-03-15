from django.db import models

# Create your models here.
class Theater(models.Model):
    theater_ID = models.AutoField(primary_key=True)
    theater_address = models.CharField(max_length=45)
    theater_name = models.CharField(max_length=45)

    class Meta:
        ordering = ['theater_ID']#sort by ID, maybe change later?
        #db_table = 'mysql_tables_use_lowercase'#put in table name

    def __str__(self):#placeholder; might replace
        return self.theater_name
