from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import *

class TheaterSearchResults(ListView):
    model = Theater
    context_object_name = "theater_list"
    def get_queryset(self):
        objs = Theater.objects
        tName = self.request.GET["name"]
        tCity = self.request.GET["tCity"]
        tState = self.request.GET["tState"]
        objs=objs.all()
        if(tName!=""):
            objs=objs.filter(theatername__icontains=tName)
        if(tCity!=""):
            objs=objs.filter(theatercity__icontains=tCity)
        if(tState!=""):
            objs=objs.filter(theaterstate__icontains=tState)
        return objs.all()
