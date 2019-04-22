from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings 
from django.core.validators import MaxValueValidator, MinValueValidator
class Theater(models.Model):
    theaterid = models.AutoField(db_column='TheaterID', primary_key=True)   
    theatername = models.CharField(db_column='TheaterName', max_length=45)   
    theaterstreet = models.CharField(db_column='TheaterStreet', max_length=45, blank=True, null=True)   
    theatercity = models.CharField(db_column='TheaterCity', max_length=45, blank=True, null=True)   
    theaterstate = models.CharField(db_column='TheaterState', max_length=45, blank=True, null=True)   
    theaterzip = models.CharField(db_column='TheaterZip', max_length=45, blank=True, null=True)   


class Profile(models.Model):
    #first name, last name and email are included in the built-in User class. Access them through the user field
    userid = models.AutoField(db_column='UserID', primary_key=True)   
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

class Movie(models.Model):
    movieid = models.AutoField(db_column='MovieID', primary_key=True)   
    movietitle = models.CharField(db_column='MovieTitle', max_length=45)   
    movieruntime = models.PositiveIntegerField(db_column='MovieRuntime', blank=True, null=True)   
    movierating = models.CharField(db_column='MovieRating', max_length=5, blank=True, null=True)   
    moviereleasedate = models.DateField(db_column='MovieReleaseDate', blank=True, null=True)   
    moviegenre = models.CharField(db_column='MovieGenre', max_length=45, blank=True, null=True)   
    moviedescription = models.CharField(db_column='MovieDescription', max_length=500, blank=True, null=True)
    #this field was added late to the project
    poster = models.ImageField(upload_to='posters/',blank=True, null=True)

class Order(models.Model):
    orderid = models.AutoField(primary_key=True)   
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='Profile_UserID', null=True)   
    qrcodetext = models.CharField(max_length=3700, blank=True, null=True)
    cost = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    
    def save(self, *args, **kwargs):
        #this generate the qrcode text based upon the seats bought
        allSeats =Seatsbought.objects.filter(order=self)
        pricePointBundles = PricePointBundle.objects.filter(order=self)
        string = []
        seat1 = allSeats.first()
        if seat1 is not None:
            string.append("ID: ")
            string.append(str(self.orderid))
            string.append("  Theater: ")
            string.append(seat1.showing.room.theater.theatername)
            string.append("  Room: ")
            string.append(str(seat1.showing.room.roomnumber))
            string.append(" Time: ")
            string.append(seat1.showing.time.strftime("%b %d %Y %H:%M:%S"))
            string.append(" Movie: ")
            string.append(seat1.showing.movie.movietitle)
            for priceBundle in pricePointBundles:
                if priceBundle.quantity is not 0:
                    string.append("  ")
                    string.append(priceBundle.pricepoint.name)
                    string.append(": ")
                    string.append(str(priceBundle.quantity))
            string.append(" Seats: ")

            for seat in allSeats:
                string.append(" Row:")
                string.append(seat.seatrow)
                string.append(" Seat: ")
                string.append(seat.seatcol)
            stringReal=''.join(string)
            self.qrcodetext=stringReal
        super(Order, self).save(*args, **kwargs)


class Room(models.Model):
    roomnumber = models.IntegerField()   
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE)   
    rows = models.IntegerField(blank=True, null=True)   
    columns = models.IntegerField(blank=True, null=True)   

class PricingGroup(models.Model):
    name = models.CharField(max_length=45)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class PricePoint(models.Model):
    name = models.CharField(max_length=45)
    price =  models.DecimalField(default=10, max_digits=10, decimal_places=2)
    group = models.ForeignKey(PricingGroup, on_delete=models.CASCADE)

class PricePointBundle(models.Model):
    pricepoint = models.ForeignKey(PricePoint, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Movieshowing(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_of")   
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.DateTimeField()
    pricing = models.ForeignKey(PricingGroup,models.SET_NULL,blank=True,null=True,)
class Promocode(models.Model):
    percent = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)

class Seatsbought(models.Model):
    seatrow = models.CharField(max_length=10)  
    seatcol = models.CharField(max_length=10) 
    showing = models.ForeignKey(Movieshowing, on_delete=models.CASCADE, related_name="showing_of")   
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_of")
    final = models.BooleanField(default=False)
    expirationTime = models.DateTimeField(default=timezone.now()+timedelta(minutes=10))

