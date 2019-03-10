from django.db import models

# Create your models here.
class Theater(models.Model):
    theater_ID = models.AutoField(primary_key=True)#correct auto-increment format?
    theater_address = models.CharField(max_length=45)
    theater_name = models.CharField(max_length=45)
