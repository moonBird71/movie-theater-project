from django.urls import include, path, re_path
from django.contrib import admin
from ticketingApps import views
app_name = "ticketingApps"
urlpatterns = [
    re_path(r'^$', views.IndexPage.as_view(), name="index"),
    re_path(r'^theater/list/$', views.TheaterListView.as_view(), name="theater-list"),
    re_path(r'^theater/entry/$', views.AddTheater.as_view(), name="add-theater"),
    re_path(r'^showings/list/$', views.ShowingsList.as_view(), name="showings-list"),
    re_path(r'^ticket/print/(?P<orderId>\d+)/$', views.PrintTicket.as_view(), name="print-ticket"),
    re_path(r'^theater/search/$',views.TheaterSearchResults.as_view(), name="search-theater"),
    re_path(r'^room/entry/$', views.AddRoom.as_view(), name ="add-room"),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^signup/$', views.Signup.as_view(), name='sign-up'),
    re_path(r'^hello/$',views.Welcome.as_view(), name='welcome'),
    re_path(r'^login_success/$',views.login_success,name='login_success'),
    re_path(r'^manager/$',views.ManagerLanding.as_view(),name='manager-landing'),
    re_path(r'^manager/theaters/$',views.ManagedTheaters.as_view(),name='theaters-filtered'),
    re_path(r'^manager/theaters/add_showing/(?P<theaterId>\d+)/$',views.AddShowing.as_view(),name='add-showing'),
    re_path(r'^manager/theaters/(?P<theaterId>\d+)/add_room/$', views.AddRoom.as_view(),name='add-room'),
    re_path(r'^manager/movie/add_movie/$', views.AddMovie.as_view(),name='add-movie'),
    re_path(r'^showings/(?P<showing>\d+)/order/$', views.SeatSelectionPage.as_view(), name='seat-selection'),
    re_path(r'^showings/order/payment/$', views.SimpleOrderPage.as_view(), name='order'),
    re_path(r'^showings/order/charge/$', views.charge, name="charge"),
    re_path(r'^showings/search/$', views.ShowingsSearchResults.as_view(), name='showing-search'),    
]
