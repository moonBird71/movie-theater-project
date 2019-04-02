from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import *
from ticketingApps.forms import *
from datetime import datetime
from django.contrib.auth.models import User

#index/home page
class IndexPage(TemplateView):
    template_name = "ticketingApps/index.html"

#List of Theaters
class TheaterListView(ListView):
    #context_object_name = "theater_list"
    model = Theater
    form_class=TheaterForm
    paginate_by = 25
    template_name = "ticketingApps/theater_list.html"
    def TheaterList(self):
        return Theater.objects.all()
	
#List of Showings
class ShowingsList(ListView):
    model = Movieshowing
    fields = '__all__'
    template_name = "ticketingApps/showings_list.html"

class ShowingsSearchResults(ListView):
    model = Movieshowing
    template_name="ticketingApps/showings_list.html"
    def get_queryset(self):
        objs = Movieshowing.objects
        tName = self.request.GET["name"]
        tCity = self.request.GET["tCity"]
        tState = self.request.GET["tState"]
        mName = self.request.GET['mName']
        objs=objs.all()
        if(tName!=""):
            objs=objs.filter(room__theater__theatername__icontains=tName)
        if(tCity!=""):
            objs=objs.filter(room__theater__theatercity__icontains=tCity)
        if(tState!=""):
            objs=objs.filter(room__theater__theaterstate__icontains=tState)
        if(mName!=""):
            objs=objs.filter(movie__movietitle__icontains=mName)
        return objs.all()

#Print ticket page
class PrintTicket(TemplateView):
    model = Ticket
    fields = '__all__'
    template_name = "ticketingApps/print_ticket.html"
    def ticketprint(request):
        if request.method == 'GET':#if directed here by another page's GET
            return render(request, "ticketingApps/print_ticket.html", request.GET)#use input from calling page

