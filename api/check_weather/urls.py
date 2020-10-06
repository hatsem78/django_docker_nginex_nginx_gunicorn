from django.urls import path

from . import views

app_name = 'check_weather'

urlpatterns = [
    path('list/', views.CheckWeatherView.as_view(), name='list'),
]