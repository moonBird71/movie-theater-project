from django.urls import include, path, re_path
from django.contrib import admin
from ticketingApps import views
app_name = "orderIn"
urlpatterns = [
    re_path(r'^user/entry/$', views.UserCreate.as_view(), name="user-create"),
    re_path(r'^user/list/$', views.UserList.as_view(), name="user-list"),
]
