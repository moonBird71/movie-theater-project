# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Creditcard(models.Model):
    name = models.CharField(max_length=45)
    cardnumber = models.CharField(db_column='cardNumber', max_length=45, blank=True, null=True)  # Field name made lowercase.
    verificationcode = models.CharField(db_column='verificationCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    expiration = models.DateField(db_column='Expiration', blank=True, null=True)  # Field name made lowercase.
    creditcardid = models.AutoField(db_column='CreditCardID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CreditCard'


class Login(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='passwordHash', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Login'


class Movie(models.Model):
    movieid = models.AutoField(db_column='MovieID', primary_key=True)  # Field name made lowercase.
    movietitle = models.CharField(db_column='MovieTitle', max_length=45, blank=True, null=True)  # Field name made lowercase.
    movieruntime = models.IntegerField(db_column='MovieRuntime', blank=True, null=True)  # Field name made lowercase.
    movierating = models.CharField(db_column='MovieRating', max_length=4, blank=True, null=True)  # Field name made lowercase.
    moviereleasedate = models.DateField(db_column='MovieReleaseDate', blank=True, null=True)  # Field name made lowercase.
    moviecol = models.CharField(db_column='Moviecol', max_length=45, blank=True, null=True)  # Field name made lowercase.
    moviegenre = models.CharField(db_column='MovieGenre', max_length=45, blank=True, null=True)  # Field name made lowercase.
    moviedescription = models.CharField(db_column='MovieDescription', max_length=500, blank=True, null=True)  # Field name made lowercase.
    moviecol1 = models.CharField(db_column='Moviecol1', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Movie'


class Movieshowing(models.Model):
    room_roomnumber = models.ForeignKey('Room', models.DO_NOTHING, db_column='Room_RoomNumber', primary_key=True)  # Field name made lowercase.
    room_theater_theaterid = models.ForeignKey('Room', models.DO_NOTHING, db_column='Room_Theater_TheaterID')  # Field name made lowercase.
    movie_idmovie = models.ForeignKey(Movie, models.DO_NOTHING, db_column='Movie_idMovie')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MovieShowing'
        unique_together = (('room_roomnumber', 'room_theater_theaterid', 'movie_idmovie'),)


class Order(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    user_userid = models.ForeignKey('User', models.DO_NOTHING, db_column='User_UserID')  # Field name made lowercase.
    creditcard_creditcardid = models.ForeignKey(Creditcard, models.DO_NOTHING, db_column='CreditCard_CreditCardID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Order'


class Room(models.Model):
    roomnumber = models.IntegerField(db_column='RoomNumber', primary_key=True)  # Field name made lowercase.
    theater_theaterid = models.ForeignKey('Theater', models.DO_NOTHING, db_column='Theater_TheaterID')  # Field name made lowercase.
    roomseatrows = models.IntegerField(db_column='RoomSeatRows', blank=True, null=True)  # Field name made lowercase.
    roomseatcolumns = models.IntegerField(db_column='RoomSeatColumns', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Room'
        unique_together = (('roomnumber', 'theater_theaterid'),)


class Seatsbought(models.Model):
    seatnumber = models.CharField(db_column='SeatNumber', max_length=10)  # Field name made lowercase.
    movieshowing_room_roomnumber = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Room_RoomNumber', primary_key=True)  # Field name made lowercase.
    movieshowing_room_theater_theaterid = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Room_Theater_TheaterID')  # Field name made lowercase.
    movieshowing_movie_idmovie = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Movie_idMovie')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SeatsBought'
        unique_together = (('movieshowing_room_roomnumber', 'movieshowing_room_theater_theaterid', 'movieshowing_movie_idmovie', 'seatnumber'),)


class Theater(models.Model):
    theaterid = models.AutoField(db_column='TheaterID', primary_key=True)  # Field name made lowercase.
    theateraddress = models.CharField(db_column='TheaterAddress', max_length=45, blank=True, null=True)  # Field name made lowercase.
    theatername = models.CharField(db_column='TheaterName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Theater'


class Ticket(models.Model):
    ticketid = models.AutoField(db_column='TicketID', primary_key=True)  # Field name made lowercase.
    order_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='Order_OrderID')  # Field name made lowercase.
    user_userid = models.ForeignKey('User', models.DO_NOTHING, db_column='User_UserID')  # Field name made lowercase.
    seatsbought_movieshowing_room_roomnumber = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Room_RoomNumber')  # Field name made lowercase.
    seatsbought_movieshowing_room_theater_theaterid = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Room_Theater_TheaterID')  # Field name made lowercase.
    seatsbought_movieshowing_movie_idmovie = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Movie_idMovie')  # Field name made lowercase.
    seatsbought_seatnumber = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_SeatNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ticket'


class User(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    userfirstname = models.CharField(db_column='UserFirstName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    userlastname = models.CharField(db_column='UserLastName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    useremail = models.CharField(db_column='UserEmail', max_length=45, blank=True, null=True)  # Field name made lowercase.
    userphone = models.CharField(db_column='UserPhone', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
