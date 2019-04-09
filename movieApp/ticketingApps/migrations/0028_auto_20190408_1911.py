# Generated by Django 2.1.5 on 2019-04-09 00:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0027_auto_20190408_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='qrcodetext',
            field=models.CharField(blank=True, max_length=8000, null=True),
        ),
        migrations.AlterField(
            model_name='seatsbought',
            name='expirationTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 9, 0, 21, 46, 4378, tzinfo=utc)),
        ),
    ]