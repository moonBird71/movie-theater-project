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
from django.http import Http404

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

class AddRoom(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Room
    form_class=AddRoomForm
    success_url='/manager/theaters/'
    def form_valid(self,form):
        form.instance.theater = Theater.objects.get(theaterid=self.kwargs["theaterId"])
        return super(AddRoom, self).form_valid(form)
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
class TheaterSearchResults(ListView):
    model = Theater
    context_object_name = "theater_list"
    paginate_by = 25
    def get_queryset(self):
        objs = Theater.objects.filter(profile__user=self.request.user)
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
class TheaterDetail(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Theater
    template_name="ticketingApps/theater_detail.html"
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(TheaterDetail, self).get_object()
        if obj not in Theater.objects.filter(profile__user=self.request.user):
            raise Http404("Theater not found.")
        return obj
class ManagedTheaters(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Theater
    context_object_name = "theater_list"
    paginate_by = 25
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_queryset(self):
        objs = self.request.user.profile.theaters
        return objs.all()