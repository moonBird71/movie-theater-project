# Generated by Django 2.1.5 on 2019-04-07 00:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0023_auto_20190406_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='code',
            field=models.CharField(default='x', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seatsbought',
            name='expirationTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 7, 1, 8, 53, 611617, tzinfo=utc)),
        ),
    ]
