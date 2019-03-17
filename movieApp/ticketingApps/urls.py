from django.urls import include, path, re_path
from django.contrib import admin
from ticketingApps import views
app_name = "orderIn"
urlpatterns = [
    re_path(r'^$', views.IndexPage.as_view(), name="index"),
    #re_path(r'^$', views.index, name="index"),
    re_path(r'^user/entry/$', views.UserCreate.as_view(), name="user-create"),
    re_path(r'^user/list/$', views.UserList.as_view(), name="user-list"),
	re_path(r'^theater/list/$', views.TheaterListView.as_view(), name="theater-list"),#correct format?
	re_path(r'^theater/entry/$', views.AddTheater.as_view(), name="add-theater"),#correct format?
]
