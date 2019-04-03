from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from ticketingApps.models import *
from ticketingApps.forms import *
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms

class ManagerLanding(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    template_name = 'ticketingApps/manager_landing.html'
class ManagedTheaters(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Theater
    context_object_name = "theater_list"
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_queryset(self):
        objs = self.request.user.profile.theaters
        return objs.all()
#Add Theater

class AddTheater(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Theater
    form_class=TheaterForm
    template_name = "ticketingApps/theater_form.html"
    success_url="/manager/theaters/"
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def form_valid(self,form):
        theater=form.save(commit=False)
        theater.save()
        self.request.user.profile.theaters.add(theater)
        return super(AddTheater,self).form_valid(form)

class AddShowing(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Movieshowing
    form_class=AddShowingForm
    template_name = "ticketingApps/add_showing.html"
    success_url='/manager/theaters/'
    def get_form(self,form_class=AddShowingForm):
        form = super(AddShowing, self).get_form(AddShowingForm)
        theaterPicked = Theater.objects.get(theaterid=self.kwargs["theaterId"])
        form.fields['room'].queryset=Room.objects.filter(theater=theaterPicked)
        return form
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")

class AddRoom(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Room
    form_class=AddRoomForm
    success_url='/manager/theaters/'
    def form_valid(self,form):
        form.instance.theater = Theater.objects.get(theaterid=self.kwargs["theaterId"])
        return super(AddRoom, self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")

class AddMovie(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Movie
    form_class=AddMovieForm
    success_url='/manager/theaters/'
    def get_initial(self):
        return {'moviereleasedate':datetime.now()}
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")

class DeleteTheater(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Theater
    success_url='/manager/theaters/'
    template_name='ticketingApps/theater_delete_confirm.html'
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteTheater, self).get_object()
        if obj not in self.request.user.profile.theaters.all():
            raise Http404
        return obj
class DeleteRoom(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Room
    success_url='/manager/theaters/'
    template_name='ticketingApps/room_delete_confirm.html'
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteRoom, self).get_object()
        if obj not in Room.objects.filter(theater__profile__user=self.request.user):
            raise Http404
        return obj
class DeleteShowing(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Movieshowing
    success_url='/manager/theaters/'
    template_name='ticketingApps/showing_delete_confirm.html'
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteRoom, self).get_object()
        if obj not in Movieshowing.objects.filter(room__theater__profile__user=self.request.user):
            raise Http404
        return obj
class TheaterDetail(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Theater
    template_name="ticketingApps/theater_detail.html"
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")