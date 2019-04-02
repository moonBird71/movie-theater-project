from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import *
from ticketingApps.forms import *

#add room
class AddRoom(CreateView):
    model = Room
    fields = '__all__'
    template_name = "ticketingApps/room_form.html"
    success_url="/manager/theaters/"
