from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import *
from ticketingApps.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

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
    paginate_by = 25 
    def get_queryset(self):
        objs = Movieshowing.objects
        objs=objs.filter(time__gte=timezone.now())
        objs=objs.order_by('time')
        return objs

class ShowingsSearchResults(ListView):
    model = Movieshowing
    template_name="ticketingApps/showings_list.html"
    paginate_by = 25  
    def get_queryset(self):
        objs = Movieshowing.objects
        tName = self.request.GET["name"]
        tCity = self.request.GET["tCity"]
        tState = self.request.GET["tState"]
        mName = self.request.GET['mName']
        day = self.request.GET['day']
        objs=objs.all()
        if(tName!=""):
            objs=objs.filter(room__theater__theatername__icontains=tName)
        if(tCity!=""):
            objs=objs.filter(room__theater__theatercity__icontains=tCity)
        if(tState!=""):
            objs=objs.filter(room__theater__theaterstate__icontains=tState)
        if(mName!=""):
            objs=objs.filter(movie__movietitle__icontains=mName)
        if(day!=""):
            objs=objs.filter(time__range=(datetime.strptime(day,"%Y-%m-%d"),datetime.strptime(day,"%Y-%m-%d")+timedelta(days=1)))
        objs=objs.filter(time__gte=timezone.now())
        objs=objs.order_by('time')
        return objs.all()
class ShowingDetail(DetailView):
    model = Movieshowing
    template_name="ticketingApps/showing_detail.html"


#Print ticket page
class PrintTicket(TemplateView):
    template_name = "ticketingApps/print_ticket.html"
    def get_context_data(self, *args, **kwargs):
        context=super(PrintTicket, self).get_context_data(*args,**kwargs)
        #Movieshowing.objects.get(id=kwargs['showing'])
        # below we build context
        order = Order.objects.get(orderid=kwargs['orderId'])
        # add seats
        seats = Seatsbought.objects.filter(order=order)
        context['seats'] = seats
        # add orderid
        context['order'] = order
        # add movieshowing time
        if seats:
            movieshowing = seats[0].showing
        else:
            print("error")
        context['showing']=movieshowing
        context['showingtime'] = movieshowing.time
        # add room number
        room = movieshowing.room
        context['roomnumber'] = room.roomnumber
        # add movie
        movie = movieshowing.movie
        context['moviename'] = movie.movietitle
        # add theatre name
        theater = room.theater
        context['theatername'] = theater.theatername
        return context
class UserTicketsListing(LoginRequiredMixin,ListView):
    Model=Order
    template_name="ticketingApps/my_tickets.html"
    paginate_by=25
    def get_queryset(self):
        objs = Order.objects
        objs = objs.filter(profile__user=self.request.user, order_of__final=1).distinct()
        return objs.order_by('-order_of__showing__time')
    def get_context_data(self, *args,**kwargs):
        context=super(UserTicketsListing, self).get_context_data(*args,**kwargs)
        if(self.object_list.first()):
            context['valid']=True
        else:
            context['valid']=False
        return context
