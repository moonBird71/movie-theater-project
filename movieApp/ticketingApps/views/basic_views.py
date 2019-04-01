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
	
#Print ticket page
class PrintTicket(TemplateView):
    model = Ticket
    fields = '__all__'
    template_name = "ticketingApps/print_ticket.html"
    def ticketprint(request):
        if request.method == 'GET':#if directed here by another page's GET
            return render(request, "ticketingApps/print_ticket.html", request.GET)#use input from calling page

