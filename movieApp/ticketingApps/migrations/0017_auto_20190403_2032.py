# Generated by Django 2.1.5 on 2019-04-04 01:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0016_auto_20190402_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricePoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('price', models.DecimalField(decimal_places=2, default=10, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PricingGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketingApps.Profile')),
            ],
        ),
        migrations.AlterField(
            model_name='movie',
            name='movierating',
            field=models.CharField(blank=True, db_column='MovieRating', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='seatsbought',
            name='expirationTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 4, 1, 42, 12, 226773, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='pricepoint',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketingApps.PricingGroup'),
        ),
    ]
