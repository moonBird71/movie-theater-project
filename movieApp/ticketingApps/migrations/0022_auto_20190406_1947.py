# Generated by Django 2.1.5 on 2019-04-07 00:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0021_auto_20190406_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seatsbought',
            name='expirationTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 7, 0, 57, 14, 888773, tzinfo=utc)),
        ),
    ]
