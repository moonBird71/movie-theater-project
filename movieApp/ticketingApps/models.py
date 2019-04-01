from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Theater(models.Model):
    theaterid = models.AutoField(db_column='TheaterID', primary_key=True)   
    theatername = models.CharField(db_column='TheaterName', max_length=45, blank=True, null=True)   
    theaterstreet = models.CharField(db_column='TheaterStreet', max_length=45, blank=True, null=True)   
    theatercity = models.CharField(db_column='TheaterCity', max_length=45, blank=True, null=True)   
    theaterstate = models.CharField(db_column='TheaterState', max_length=45, blank=True, null=True)   
    theaterzip = models.CharField(db_column='TheaterZip', max_length=45, blank=True, null=True)   
		
	#def __str__(self):	#returns theatername as a string. Placeholder
		#return self.theatername
		
	#def get_absolute_url(self): #returns url to individual theater; need to include in urls.py
		#return reverse('orderIn:add-theater')#correct format? 

class Profile(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)   
    #first name, last name and email are included in the built-in User class. Access them through the user field
    #userfirstname = models.CharField(db_column='UserFirstName', max_length=45, blank=True, null=True, verbose_name="first name")   
    #userlastname = models.CharField(db_column='UserLastName', max_length=45, blank=True, null=True, verbose_name="last name")   
    #useremail = models.CharField(db_column='UserEmail', max_length=45, blank=True, null=True, verbose_name="email")   
    userphone = models.CharField(db_column='UserPhone', max_length=45, blank=True, null=True, verbose_name="phone")   
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
    cardnumber = models.CharField(db_column='cardNumber', max_length=45, blank=True, null=True)   
    verificationcode = models.CharField(db_column='verificationCode', max_length=45, blank=True, null=True)   
    expiration = models.DateField(db_column='Expiration', blank=True, null=True)   
    creditcardid = models.AutoField(db_column='CreditCardID', primary_key=True)   

class Movie(models.Model):
    movieid = models.AutoField(db_column='MovieID', primary_key=True)   
    movietitle = models.CharField(db_column='MovieTitle', max_length=45, blank=True, null=True)   
    movieruntime = models.IntegerField(db_column='MovieRuntime', blank=True, null=True)   
    movierating = models.CharField(db_column='MovieRating', max_length=4, blank=True, null=True)   
    moviereleasedate = models.DateField(db_column='MovieReleaseDate', blank=True, null=True)   
    moviegenre = models.CharField(db_column='MovieGenre', max_length=45, blank=True, null=True)   
    moviedescription = models.CharField(db_column='MovieDescription', max_length=500, blank=True, null=True)   


class Order(models.Model):
    orderid = models.AutoField(primary_key=True)   
    profile = models.ForeignKey(Profile, models.DO_NOTHING, db_column='Profile_UserID')   
    creditcard = models.ForeignKey(Creditcard, models.DO_NOTHING, db_column='CreditCard_CreditCardID')   
 


class Room(models.Model):
    roomnumber = models.IntegerField()   
    theater = models.ForeignKey('Theater', models.DO_NOTHING)   
    rows = models.IntegerField(blank=True, null=True)   
    columns = models.IntegerField(blank=True, null=True)   

class Movieshowing(models.Model):
    room = models.ForeignKey(Room, models.DO_NOTHING, related_name="room_of")   
    #room_theater_theaterid = models.ForeignKey(Room, models.DO_NOTHING, db_column='Room_Theater_TheaterID', related_name="theater_of")   
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    time = models.DateTimeField()
       

    #class Meta:
        #unique_together = (('room_roomnumber', 'room_theater_theaterid', 'movie_idmovie'),)


class Seatsbought(models.Model):
    seatrow = models.CharField(max_length=10)  
    seatcol = models.CharField(max_length=10) 
    showing = models.ForeignKey(Movieshowing, models.DO_NOTHING, related_name="showing_of")   
    order = models.ForeignKey(Order, models.DO_NOTHING, related_name="order_of")
    #movieshowing_room_theater_theaterid = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Room_Theater_TheaterID', related_name="theater_of")   
    #movieshowing_movie_idmovie = models.ForeignKey(Movieshowing, models.DO_NOTHING, db_column='MovieShowing_Movie_idMovie', related_name="movie_of")   

    #class Meta:
        #unique_together = (('movieshowing_room_roomnumber', 'movieshowing_room_theater_theaterid', 'movieshowing_movie_idmovie', 'seatnumber'),)



class Ticket(models.Model):
    ticketid = models.AutoField(primary_key=True)   
    order = models.ForeignKey(Order, models.DO_NOTHING)   
    #orders already associate tickets with profiles
    #profile = models.ForeignKey(Profile, models.DO_NOTHING, db_column='Profile_UserID')   
    #seatsbought_movieshowing_room_roomnumber = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Room_RoomNumber', related_name="room_of")   
    #seatsbought_movieshowing_room_theater_theaterid = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Room_Theater_TheaterID', related_name="theater_of")   
    #seatsbought_movieshowing_movie_idmovie = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_MovieShowing_Movie_idMovie', related_name="movie_of")   
    #seats = models.ForeignKey(Seatsbought, models.DO_NOTHING, db_column='SeatsBought_SeatNumber', related_name="seat_of")   


#class Usertheater(models.Model):
#    theater_theaterid = models.ForeignKey(Theater, models.DO_NOTHING, db_column='Theater_TheaterID',primary_key=True)
#    profile_userid = models.ForeignKey(Profile, models.DO_NOTHING, db_column='Profile_UserID')

#    class Meta:
#        unique_together = (('theater_theaterid','profile_userid'),)
