from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import User, Theater, Ticket, Movieshowing
from datetime import datetime

#index/home page
class IndexPage(TemplateView):
    template_name = "ticketingApps/index.html"

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

#List of Theaters
class TheaterListView(ListView):
    #context_object_name = "theater_list"
    model = Theater
    paginate_by = 25
    template_name = "ticketingApps/theater_list.html"
    def TheaterList(self):
        return Theater.objects.all()

#Add Theater
class AddTheater(CreateView):
    model = Theater
    fields = '__all__'
    template_name = "ticketingApps/theater_form.html"
	
#List of Showings
class ShowingsList(ListView):
    model = Movieshowing
    fields = '__all__'
    template_name = "ticketingApps/showings_list.html"
	
#Print ticket page
class PrintTicket(TemplateView):
    model = Ticket
    fields = '__all__'
    template_name = "ticketingApps/print_ticket.html"
    def ticketprint(request):
        if request.method == 'GET':#if directed here by another page's GET
            return render(request, "ticketingApps/print_ticket.html", request.GET)#use input from calling page

