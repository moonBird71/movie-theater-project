from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Theater(models.Model):
    theaterid = models.AutoField(db_column='TheaterID', primary_key=True)  # Field name made lowercase.
    theatername = models.CharField(db_column='TheaterName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    theaterstreet = models.CharField(db_column='TheaterStreet', max_length=45, blank=True, null=True)  # Field name made lowercase.
    theatercity = models.CharField(db_column='TheaterCity', max_length=45, blank=True, null=True)  # Field name made lowercase.
    theaterstate = models.CharField(db_column='TheaterState', max_length=45, blank=True, null=True)  # Field name made lowercase.
    theaterzip = models.CharField(db_column='TheaterZip', max_length=45, blank=True, null=True)  # Field name made lowercase.
		
	#def __str__(self):	#returns theatername as a string. Placeholder
		#return self.theatername
		
	#def get_absolute_url(self): #returns url to individual theater; need to include in urls.py
		#return reverse('orderIn:add-theater')#correct format? 


class Profile(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    #first name, last name and email are included in the built-in User class. Access them through the user field
    #userfirstname = models.CharField(db_column='UserFirstName', max_length=45, blank=True, null=True, verbose_name="first name")  # Field name made lowercase.
    #userlastname = models.CharField(db_column='UserLastName', max_length=45, blank=True, null=True, verbose_name="last name")  # Field name made lowercase.
    #useremail = models.CharField(db_column='UserEmail', max_length=45, blank=True, null=True, verbose_name="email")  # Field name made lowercase.
    userphone = models.CharField(db_column='UserPhone', max_length=45, blank=True, null=True, verbose_name="phone")  # Field name made lowercase.
    isemployee = models.BooleanField(db_column='isEmployee', blank=True, null=True, verbose_name="employee?")
    theaters = models.ManyToManyField(Theater)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
@receiver(post_save,sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    #this updates profile when user is updated
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Creditcard(models.Model):
    name = models.CharField(max_length=45)
    cardnumber = models.CharField(db_column='cardNumber', max_length=45, blank=True, null=True)  # Field name made lowercase.
    verificationcode = models.CharField(db_column='verificationCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    expiration = models.DateField(db_column='Expiration', blank=True, null=True)  # Field name made lowercase.
    creditcardid = models.AutoField(db_column='CreditCardID', primary_key=True)  # Field name made lowercase.

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



class Movieshowing(models.Model):
    room_roomnumber = models.ForeignKey('Room', models.DO_NOTHING, db_column='Room_RoomNumber', primary_key=True, related_name="room_of")  # Field name made lowercase.
    room_theater_theaterid = models.ForeignKey('Room', models.DO_NOTHING, db_column='Room_Theater_TheaterID', related_name="theater_of")  # Field name made lowercase.
    movie_idmovie = models.ForeignKey(Movie, models.DO_NOTHING, db_column='Movie_idMovie')  # Field name made lowercase.

    class Meta:
        unique_together = (('room_roomnumber', 'room_theater_theaterid', 'movie_idmovie'),)


class Order(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    profile_userid = models.ForeignKey(Profile, models.DO_NOTHING, db_column='Profile_UserID')  # Field name made lowercase.
    creditcard_creditcardid = models.ForeignKey(Creditcard, models.DO_NOTHING, db_column='CreditCard_CreditCardID')  # Field name made lowercase.


class Room(models.Model):
    roomnumber = models.IntegerField(db_column='RoomNumber', primary_key=True)  # Field name made lowercase.
    theater_theaterid = models.ForeignKey('Theater', models.DO_NOTHING, db_column='Theater_TheaterID')  # Field name made lowercase.
    roomseatrows = models.IntegerField(db_column='RoomSeatRows', blank=True, null=True)  # Field name made lowercase.
    roomseatcolumns = models.IntegerField(db_column='RoomSeatColumns', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        unique_together = (('roomnumber', 'theater_theaterid'),)


class Seatsbought(models.Model):
    seatnumber = models.CharField(db_column='SeatNumber', max_length=10)  # Field name made lowercase.
    movieshowing_room_roomnumber = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Room_RoomNumber', primary_key=True, related_name="room_of")  # Field name made lowercase.
    movieshowing_room_theater_theaterid = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Room_Theater_TheaterID', related_name="theater_of")  # Field name made lowercase.
    movieshowing_movie_idmovie = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Movie_idMovie', related_name="movie_of")  # Field name made lowercase.

    class Meta:
        unique_together = (('movieshowing_room_roomnumber', 'movieshowing_room_theater_theaterid', 'movieshowing_movie_idmovie', 'seatnumber'),)



class Ticket(models.Model):
    ticketid = models.AutoField(db_column='TicketID', primary_key=True)  # Field name made lowercase.
    order_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='Order_OrderID')  # Field name made lowercase.
    profile_userid = models.ForeignKey(Profile, models.DO_NOTHING, db_column='Profile_UserID')  # Field name made lowercase.
    seatsbought_movieshowing_room_roomnumber = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Room_RoomNumber', related_name="room_of")  # Field name made lowercase.
    seatsbought_movieshowing_room_theater_theaterid = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Room_Theater_TheaterID', related_name="theater_of")  # Field name made lowercase.
    seatsbought_movieshowing_movie_idmovie = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Movie_idMovie', related_name="movie_of")  # Field name made lowercase.
    seatsbought_seatnumber = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_SeatNumber', related_name="seat_of")  # Field name made lowercase.


#class Usertheater(models.Model):
#    theater_theaterid = models.ForeignKey(Theater, models.DO_NOTHING, db_column='Theater_TheaterID',primary_key=True)
#    profile_userid = models.ForeignKey(Profile, models.DO_NOTHING, db_column='Profile_UserID')

#    class Meta:
#        unique_together = (('theater_theaterid','profile_userid'),)
