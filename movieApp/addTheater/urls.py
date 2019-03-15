from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index')
    path('', views.addTheater, name='addTheater'),#url poining to addTheater view
]
