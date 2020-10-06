# coding=utf-8
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()

app_name = "api"

urlpatterns = [

    url(r'^', include(router.urls)),
    path('meetup/', include('api.meetup.urls')),
    path('meetup_enroll_invite_users/', include('api.meetup_enroll_invite_users.urls')),
    path('registration_check_in_user/', include('api.registration_check_in_user.urls')),
    path('check_weather/', include('api.check_weather.urls')),
    path('notification/', include('api.notification.urls')),
    path('user/', include('api.user.urls')),

]
