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
class PricingForShowingField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.name
class AddShowingForm(ModelForm):
        room = RoomForShowingField(queryset=Room.objects.none())
        movie = MovieForShowingField(queryset=Movie.objects.order_by('-moviereleasedate'))
        pricing = PricingForShowingField(queryset=PricingGroup.objects.none())
        class Meta:
            model=Movieshowing
            fields=['room','movie','time','pricing']
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
class TheaterForPromoField(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.theatername
class CreatePromoCodeForm(ModelForm):
        theater = TheaterForPromoField(queryset=Theater.objects.none())
        class Meta:
            model=Promocode
            fields='__all__'

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
    promocode = forms.CharField(label="Promo Code", required=False)
    def __init__(self,pricingList,numberTix,*args,**kwargs):
        super(TicketTypeForm, self).__init__(*args, **kwargs)
        self.pList = pricingList
        self.numTix=numberTix
        for price in self.pList:
            keyF = price.name
            print(keyF)
            self.fields[keyF] = forms.ChoiceField(choices=((0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)))
    def clean(self):
        cleaned_data = super().clean()
        numTix =0
        for price in self.pList:
            numTix=numTix+int(cleaned_data.get(price.name))
        if numTix is not self.numTix:
            print("error in forM")
            raise forms.ValidationError(
                "Did not select as many tickets as seats chosen."
            )
        return cleaned_data

class AssociateEmployeeForm(forms.Form):
    username = forms.CharField(label="Username of New Employee")
    def clean(self):
        cleaned_data = super().clean()
        matching = Profile.objects.filter(user__username=cleaned_data.get('username'))
        if matching.count() is not 1:
            raise forms.ValidationError("No matching user was found.")
        if not matching.first().isemployee:
            raise forms.ValidationError("The matching user is not an employee")
        return cleaned_data
