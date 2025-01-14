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

class ManagerLanding(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    template_name = 'ticketingApps/manager_landing.html'

class ManagedShowings(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Movieshowing
    template_name="ticketingApps/managed_showings_list.html"
    paginate_by=25
    def get_queryset(self):
        objs = Movieshowing.objects.filter(room__theater__profile__user=self.request.user)
        objs=objs.order_by('-time')
        return objs
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")

class ManagedShowingsSearchResults(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Movieshowing
    template_name="ticketingApps/managed_showings_list.html"
    paginate_by=25
    def get_queryset(self):
        objs = Movieshowing.objects.filter(room__theater__profile__user=self.request.user)
        tName = self.request.GET["name"]
        tCity = self.request.GET["tCity"]
        tState = self.request.GET["tState"]
        mName = self.request.GET['mName']
        day = self.request.GET['day']
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
        objs=objs.order_by('-time')
        return objs 
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")      

class AddShowing(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Movieshowing
    form_class=AddShowingForm
    template_name = "ticketingApps/add_showing.html"
    success_url='/manager/'
    def get_form(self,form_class=AddShowingForm):
        form = super(AddShowing, self).get_form(AddShowingForm)
        theaterPicked = Theater.objects.get(theaterid=self.kwargs["theaterId"])
        form.fields['room'].queryset=Room.objects.filter(theater=theaterPicked)
        form.fields['pricing'].queryset=PricingGroup.objects.filter(profile=self.request.user.profile)
        return form
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")


class AddMovie(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Movie
    form_class=AddMovieForm
    success_url='/manager/'
    def get_initial(self):
        return {'moviereleasedate':datetime.now()}
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
class EditMovie(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Movie
    form_class=AddMovieForm
    success_url='/manager/'
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
class ListMovies(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model=Movie
    paginate_by=25
    def get_queryset(self):
        objs = Movie.objects.order_by('-moviereleasedate')
        return objs
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
class SearchMovies(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Movie
    template_name="ticketingApps/movie_list.html"
    paginate_by=25
    def get_queryset(self):
        objs=Movie.objects
        mName = self.request.GET['mName']
        if(mName!=""):
            objs=objs.filter(movietitle__icontains=mName)
        objs=objs.order_by('-moviereleasedate')
        return objs 
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")      

class DeleteShowing(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Movieshowing
    success_url='/manager/'
    template_name='ticketingApps/showing_delete_confirm.html'
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteShowing, self).get_object()
        if obj not in Movieshowing.objects.filter(room__theater__profile__user=self.request.user):
            raise Http404
        return obj

class ShowingAnalytics(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    model = Movieshowing
    template_name="ticketingApps/showing_stats.html"
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_context_data(self,*args,**kwargs):
        context=super(ShowingAnalytics, self).get_context_data(*args,**kwargs)
        showingP=context['object']
        totalSeats = int(showingP.room.rows)*int(showingP.room.columns)
        seatsSold = Seatsbought.objects.filter(showing=showingP, final=True)
        context['percentSold']='%.2f'%(100*seatsSold.count()/totalSeats)
        revenue = 0
        orders = Order.objects.filter(order_of__showing=showingP).distinct()
        context['orders']=orders
        for order in orders:
            revenue = revenue + order.cost
        context['revenue']=revenue
        return context
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ShowingAnalytics, self).get_object()
        if obj not in Movieshowing.objects.filter(room__theater__profile__user=self.request.user):
            raise Http404
        return obj
class CreatePricingGroup(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = PricingGroup
    template_name="ticketingApps/create_pricing_group.html"
    fields = ['name']
    success_url='/manager/'
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def form_valid(self,form):
        pricingGroup=form.save(commit=False)
        pricingGroup.profile=self.request.user.profile
        pricingGroup.save()
        return super(CreatePricingGroup,self).form_valid(form)
class CreatePricePoint(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = PricePoint
    template_name="ticketingApps/create_price_point.html"
    form_class = AddPricePointForm
    success_url='/manager/'
    def get_form(self,form_class=AddPricePointForm):
        form = super(CreatePricePoint, self).get_form(AddPricePointForm)
        form.fields['group'].queryset=PricingGroup.objects.filter(profile=self.request.user.profile)
        return form
    def test_func(self):
        return getattr(self.request.user.profile,"isemployee")
class CreatePromoCode(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model=Promocode
    template_name="ticketingApps/create_promo_code.html"
    form_class = CreatePromoCodeForm
    success_url='/manager/'
    def get_form(self,form_class=AddPricePointForm):
        form = super(CreatePromoCode, self).get_form(CreatePromoCodeForm)
        form.fields['theater'].queryset=Theater.objects.filter(profile=self.request.user.profile)
        return form
    def test_func(self):
        return getattr(self.request.user.profile,"isemployee")
class ListPricingGroup(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = PricingGroup
    template_name="ticketingApps/pricing_group_list.html"
    paginate_by=25
    def get_queryset(self):
        objs = PricingGroup.objects.filter(profile__user=self.request.user)
        return objs
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
class ListPromoCodes(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Promocode
    template_name="ticketingApps/promo_code_list.html"
    paginate_by=25
    def get_queryset(self):
        objs = Promocode.objects.filter(theater__profile__user=self.request.user)
        return objs
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
class DeletePromoCodes(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Promocode
    success_url='/manager/'
    template_name='ticketingApps/promo_delete_confirm.html'
    def test_func(self):
        return getattr(self.request.user.profile, "isemployee")
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeletePromoCodes, self).get_object()
        if obj not in Promocode.objects.filter(theater__profile__user=self.request.user):
            raise Http404
        return obj
class AssociateEmployee(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name='ticketingApps/add_employee.html'
    success_url='/manager/'
    form_class=AssociateEmployeeForm
    def test_func(self):
        if self.request.user.profile not in Theater.objects.get(theaterid=self.kwargs['pk']).profile_set.all():
            return False
        return getattr(self.request.user.profile, "isemployee")
    def form_valid(self, form):
        uname=form.cleaned_data['username']
        profileEntered = Profile.objects.filter(user__username=uname)
        theaterPicked = Theater.objects.get(theaterid=self.kwargs['pk'])
        profileEntered.first().theaters.add(theaterPicked)
        profileEntered.first().save()
        return super(AssociateEmployee,self).form_valid(form)