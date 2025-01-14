# Generated by Django 2.1.5 on 2019-04-09 01:26

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0030_auto_20190408_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='priceBundles',
        ),
        migrations.AddField(
            model_name='pricepointbundle',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ticketingApps.Order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seatsbought',
            name='expirationTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 9, 1, 35, 30, 923455, tzinfo=utc)),
        ),
    ]
