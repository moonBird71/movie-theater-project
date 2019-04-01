from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import *
from ticketingApps.forms import *
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import json

class SeatSelectionPage(TemplateView):
    template_name='ticketingApps/seat_selection.html'

    def get_context_data(self, *args, **kwargs):
        context=super(SeatSelectionPage, self).get_context_data(*args,**kwargs)
        showingP = Movieshowing.objects.get(id=kwargs['showing'])
        context['showing']= showingP
        context['numberRows']= showingP.room.rows
        context['numberCols']= showingP.room.columns
        allSeatsBought=Seatsbought.objects.filter(showing=showingP)
        seatsBoughtList=[]
        seatsPicked=dict()
        for i in range(showingP.room.rows):
            seatsPicked[i+1]=dict()
            for j in range(showingP.room.columns):
                seatsPicked[i+1][j+1]="#0544F0"
        for seat in allSeatsBought:
            seatsBoughtList.append([seat.seatrow,seat.seatcol])
            seatsPicked[seat.seatrow][seat.seatcol]="#666666"
        context['seatsBought']=json.dumps(seatsBoughtList)
        context['seatsPicked']=json.dumps(seatsPicked)
        return context

