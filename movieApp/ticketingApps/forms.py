from django import forms
from ticketingApps.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import datetime, timedelta
from django.utils import timezone
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
        yearNow = datetime.now().year
        yearsT = (str(yearNow), str(yearNow+1),str(yearNow+2))+(tuple(map(str, range(1900,yearNow))))
        widgets = {'moviereleasedate':forms.SelectDateWidget(years=yearsT)}
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
        movie = MovieForShowingField(queryset=Movie.objects.order_by('-moviereleasedate'))
        class Meta:
            model=Movieshowing
            fields=['room','movie','time']
            labels={
                'time':'Date and time (mm/dd/yyyy hh:mm)'
            }
class GroupForPriceField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.name
class AddPricePointForm(ModelForm):
        group = GroupForPriceField(queryset=PricingGroup.objects.none())
        class Meta:
            model=PricePoint
            fields='__all__'

class TheaterForm(ModelForm):
    class Meta:
         model=Theater
         fields=['theatername','theaterstreet','theatercity','theaterstate','theaterzip','price']
         labels={
             'theaterstreet':'Street',
             'theatername':'Name',
             'theatercity':'City',
             'theaterstate':"State",
             "theaterzip":"Zip code",
             'price':"Price per Ticket"
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
        profile = user.profile
        profile.isemployee=self.cleaned_data['isemployee']
        profile.userphone=self.cleaned_data['userphone']
        user.save()
        profile.save()
        return user, profile
class TicketTypeForm(forms.Form):
    def __init__(self, round_list, *args, **kwargs):
        super(TicketTypeForm, self).__init__(*args, **kwargs)
        pList = kwargs["pricingList"]
        for price in pList:
            keyF = price.name
            self.fields[keyF] = forms.ChoiceField(choices=(0,1,2,3,4,5,6,7,8,9,10))

