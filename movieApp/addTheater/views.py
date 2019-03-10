from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView#, UpdateView, DeleteView #add edit and delete functions later
from django.urls import reverse_lazy, reverse
#from django.http import HttpResponse#need to replace with a list of theaters connected to DB 
from .models import Theater

# Create your views here.
class TheaterListView(ListView):
    context_object_name = "theater_list"
    model = Theater
    #template_name = "addTheater/index.html"

    def TheaterList(self):
        #return HttpResponse("Placeholder: you're at the addTheater view")
        return Theater.objects.all()

class AddTheater(CreateView):
    model = Theater
    fields = ['ID', 'Address', 'Name']
    #success_url = reverse_lazy('addTheater:index')
