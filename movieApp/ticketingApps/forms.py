from django import forms
from ticketingApps.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import datetime
class SimpleOrder(ModelForm):
    class Meta:
        model=Creditcard
        fields="__all__"
        labels={
            'name':"Name",
            'cardnumber':"Card Number",
            "verificationcode":"Verification Code",
            "expiration":"Expiration (use 1 for day if needed)"
        }
        widgets={'expiration':forms.SelectDateWidget()}
    def is_valid(self):
        ticketsList = []
        for key in toBuyArray:
            if(Seatsbought.objects.filter(showing=showingP,seatrow=toBuyArray[key][0], seatcol=toBuyArray[key][1]).count()>0):
                validSeats = False
        if validSeats:
            if self.request.user:
                Order.objects.create(credit)
            Order.objects.create()
            for key in toBuyArray:
                Seatsbought.objects.create(seatrow=toBuyArray[key][0], seatcol=toBuyArray[key][1], showing=showingP,)
            

        context['ticketList']=ticketsList
class AddMovieForm(ModelForm):
    class Meta:
        model=Movie
        fields=['movietitle','movieruntime','movierating','moviereleasedate','moviegenre','moviedescription']
        labels={
            'movietitle':'Title',
            'movieruntime':"Runtime (minutes)",
            'movierating':'MPAA Rating',
            'moviereleasedate':"Release date",
            'moviegenre':"Genre",
            'moviedescription':"Description"
        }
        widgets = {'moviereleasedate':forms.SelectDateWidget()}
class AddRoomForm(ModelForm):
    class Meta:
        model=Room
        fields=['roomnumber','rows','columns']
        labels={
            'roomnumber':'Room Number',
            'rows':'Number of Rows of Seats',
            'columns':"Number of Seats per Row"
        }
class RoomForShowingField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return "Room #%i" % obj.roomnumber
class MovieForShowingField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.movietitle
class AddShowingForm(ModelForm):
        room = RoomForShowingField(queryset=Room.objects.none())
        movie = MovieForShowingField(queryset=Movie.objects.all())
        class Meta:
            model=Movieshowing
            fields=['room','movie','time']
            labels={
                'time':'Date and time (mm/dd/yyyy hh:mm)'
            }
            #widgets={'time':forms.}
class TheaterForm(ModelForm):
    class Meta:
         model=Theater
         fields=['theatername','theaterstreet','theatercity','theaterstate','theaterzip']
         labels={
             'theaterstreet':'Street',
             'theatername':'Name',
             'theatercity':'City',
             'theaterstate':"State",
             "theaterzip":"Zip code",
         }
class SignupForm(UserCreationForm):
    isemployee=forms.BooleanField(required=False,label="I am registering as a theater employee")
    userphone=forms.CharField(label="Phone Number")
    class Meta:
        model=User
        fields=['email','username','password1','password2','isemployee','first_name','last_name','userphone']
        labels={
            'email':'Email',
            'username':'Username',
            'password1':'Password',
            'password2':'Confirm Password',
            #'isemployee':"I am registering as a theater employee",
            'first_name':"First Name",
            'last_name':"Last Name",
            #'userphone':'Phone Number',
        }
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(SignupForm, self).save(commit=True)
        #User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'], email=self.cleaned_data['email'],first_name=self.cleaned_data['first_name'],last_name=self.cleaned_data['last_name'])
        #profile = Profile(user=user, isemployee=self.cleaned_data['isemployee'], 
        #    userphone=self.cleaned_data['userphone'])
        profile = user.profile
        profile.isemployee=self.cleaned_data['isemployee']
        profile.userphone=self.cleaned_data['userphone']
        user.save()
        profile.save()
        return user, profile

