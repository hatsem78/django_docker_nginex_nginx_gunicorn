from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'meetup'

urlpatterns = [
    url(r"^$", views.Index.as_view(), name="index"),
    url(r"logout/$", views.logout, name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^dashboard', views.Dashboard.as_view(), name='dashboard'),
    url(r'^check_in', views.RegistrationUser.as_view(), name='check_in'),
    url(r'^create_meeetup_beer', views.CreateMeeetupBeer.as_view(), name='create_meeetup_beer'),
    url(r'^notification_all', views.NotificationAll.as_view(), name='notification_all'),
]