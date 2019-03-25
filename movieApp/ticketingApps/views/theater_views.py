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
        objs=objs.filter(theatername__icontains=tName)
        return objs.all()
