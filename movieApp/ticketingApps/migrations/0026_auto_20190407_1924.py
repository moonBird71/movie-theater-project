# Generated by Django 2.1.5 on 2019-04-08 00:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0025_auto_20190406_2216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='creditcard',
        ),
        migrations.AlterField(
            model_name='seatsbought',
            name='expirationTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 8, 0, 34, 49, 211388, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Creditcard',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]