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

class Signup(FormView):
    template_name='ticketingApps/signup.html'
    form_class= SignupForm
    success_url='/accounts/login/'
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)
class Welcome(TemplateView):
    template_name='ticketingApps/hello.html'

def login_success(request):
    if request.user.profile.isemployee:
        return redirect('/manager/')
    else:
        return redirect('ticketingApps:index')
       