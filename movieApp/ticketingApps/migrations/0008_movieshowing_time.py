# Generated by Django 2.1.5 on 2019-04-01 03:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0007_auto_20190331_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieshowing',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 31, 22, 25, 31, 523327)),
            preserve_default=False,
        ),
    ]
