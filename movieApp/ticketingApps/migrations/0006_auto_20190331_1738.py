# Generated by Django 2.1.5 on 2019-03-31 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0005_auto_20190331_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movieshowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ticketingApps.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomnumber', models.IntegerField()),
                ('rows', models.IntegerField(blank=True, null=True)),
                ('columns', models.IntegerField(blank=True, null=True)),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ticketingApps.Theater')),
            ],
        ),
        migrations.CreateModel(
            name='Seatsbought',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seatnumber', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='orderid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ticketingApps.Order'),
        ),
        migrations.AddField(
            model_name='seatsbought',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_of', to='ticketingApps.Order'),
        ),
        migrations.AddField(
            model_name='seatsbought',
            name='showing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='showing_of', to='ticketingApps.Movieshowing'),
        ),
        migrations.AddField(
            model_name='movieshowing',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='room_of', to='ticketingApps.Room'),
        ),
    ]
