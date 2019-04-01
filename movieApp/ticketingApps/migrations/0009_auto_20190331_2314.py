# Generated by Django 2.1.5 on 2019-04-01 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0008_movieshowing_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seatsbought',
            name='seatnumber',
        ),
        migrations.AddField(
            model_name='seatsbought',
            name='seatcol',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seatsbought',
            name='seatrow',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]