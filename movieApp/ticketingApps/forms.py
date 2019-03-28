from django import forms
from ticketingApps.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class TheaterForm(ModelForm):
    class Meta:
         model=Theater
         fields='__all__'
         labels={
             'theateraddress':'Address',
             'theatername':'Name'
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

