# Generated by Django 2.1.5 on 2019-04-09 01:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0029_auto_20190408_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricePointBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('pricepoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketingApps.PricePoint')),
            ],
        ),
        migrations.AlterField(
            model_name='seatsbought',
            name='expirationTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 9, 1, 25, 35, 717327, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='order',
            name='priceBundles',
            field=models.ManyToManyField(to='ticketingApps.PricePointBundle'),
        ),
    ]
