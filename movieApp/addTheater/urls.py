from django.urls import path

from addTheater import views

urlpatterns = [
        path('', views.AddTheater.as_view(), name='addTheater'),#url poining to addTheater view
]
