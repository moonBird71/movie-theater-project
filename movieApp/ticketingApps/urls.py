from django.urls import include, path, re_path
from django.contrib import admin
from ticketingApps import views
app_name = "ticketingApps"
urlpatterns = [
    re_path(r'^$', views.IndexPage.as_view(), name="index"),
    #re_path(r'^$', views.index, name="index"),
    re_path(r'^user/entry/$', views.UserCreate.as_view(), name="user-create"),
    re_path(r'^user/list/$', views.UserList.as_view(), name="user-list"),
    re_path(r'^theater/list/$', views.TheaterListView.as_view(), name="theater-list"),
    re_path(r'^theater/entry/$', views.AddTheater.as_view(), name="add-theater"),
    re_path(r'^showings/list/$', views.ShowingsList.as_view(), name="showings-list"),
    re_path(r'^ticket/print/$', views.PrintTicket.as_view(), name="print-ticket"),
    re_path(r'^theater/search/$',views.TheaterSearchResults.as_view(), name="search-theater"),
    
]
