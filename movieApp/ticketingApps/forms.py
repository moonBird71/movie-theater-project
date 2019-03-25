from django import forms
from ticketingApps.models import *
from django.forms import ModelForm
class TheaterForm(ModelForm):
    class Meta:
         model=Theater
         fields='__all__'
         labels={
             'theateraddress':'Address',
             'theatername':'Name'
         }