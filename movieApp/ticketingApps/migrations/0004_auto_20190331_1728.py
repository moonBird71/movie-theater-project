# Generated by Django 2.1.5 on 2019-03-31 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingApps', '0003_auto_20190328_1505 - Copy'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movieshowing',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='movieshowing',
            name='movie_idmovie',
        ),
        migrations.RemoveField(
            model_name='movieshowing',
            name='room_roomnumber',
        ),
        migrations.RemoveField(
            model_name='movieshowing',
            name='room_theater_theaterid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='creditcard_creditcardid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='profile_userid',
        ),
        migrations.AlterUniqueTogether(
            name='seatsbought',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='seatsbought',
            name='movieshowing_movie_idmovie',
        ),
        migrations.RemoveField(
            model_name='seatsbought',
            name='movieshowing_room_roomnumber',
        ),
        migrations.RemoveField(
            model_name='seatsbought',
            name='movieshowing_room_theater_theaterid',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='order_orderid',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='profile_userid',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='seatsbought_movieshowing_movie_idmovie',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='seatsbought_movieshowing_room_roomnumber',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='seatsbought_movieshowing_room_theater_theaterid',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='seatsbought_seatnumber',
        ),
        migrations.DeleteModel(
            name='Movieshowing',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Seatsbought',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
