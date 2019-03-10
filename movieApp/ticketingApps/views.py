from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import User
from datetime import datetime

#Add User Page
class UserCreate(CreateView):
    model=User
    fields = '__all__'
    template_name="ticketingApps/user_form.html"
    
#Show List of Users
class UserList(ListView):
    model=User
    paginate_by=25
    template_name="ticketingApps/user_list.html"
    def get_queryset(self):
        return User.objects.all()
    
