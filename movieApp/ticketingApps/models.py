from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone
class Theater(models.Model):
    theaterid = models.AutoField(db_column='TheaterID', primary_key=True)   
    theatername = models.CharField(db_column='TheaterName', max_length=45, blank=True, null=True)   
    theaterstreet = models.CharField(db_column='TheaterStreet', max_length=45, blank=True, null=True)   
    theatercity = models.CharField(db_column='TheaterCity', max_length=45, blank=True, null=True)   
    theaterstate = models.CharField(db_column='TheaterState', max_length=45, blank=True, null=True)   
    theaterzip = models.CharField(db_column='TheaterZip', max_length=45, blank=True, null=True)   
    price = models.DecimalField(default=10, max_digits=10, decimal_places=2)
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
    profile = models.ForeignKey(Profile, models.DO_NOTHING, db_column='Profile_UserID', null=True)   
    creditcard = models.ForeignKey(Creditcard, models.DO_NOTHING, db_column='CreditCard_CreditCardID', null=True)   
 


class Room(models.Model):
    roomnumber = models.IntegerField()   
    theater = models.ForeignKey('Theater', models.DO_NOTHING)   
    rows = models.IntegerField(blank=True, null=True)   
    columns = models.IntegerField(blank=True, null=True)   

class Movieshowing(models.Model):
    room = models.ForeignKey(Room, models.DO_NOTHING, related_name="room_of")   
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    time = models.DateTimeField()


class Seatsbought(models.Model):
    seatrow = models.CharField(max_length=10)  
    seatcol = models.CharField(max_length=10) 
    showing = models.ForeignKey(Movieshowing, models.DO_NOTHING, related_name="showing_of")   
    order = models.ForeignKey(Order, models.DO_NOTHING, related_name="order_of")
    final = models.BooleanField(default=False)
    expirationTime = models.DateTimeField(default=timezone.now()+timedelta(minutes=10))

class Ticket(models.Model):
    ticketid = models.AutoField(primary_key=True)   
    order = models.ForeignKey(Order, models.DO_NOTHING)   
