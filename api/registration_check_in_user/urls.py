from django.urls import path

from . import views

app_name = 'registration_check_in_user'

urlpatterns = [
    path('registration/', views.RegistrationCheckInUserView.as_view(), name='registration'),
    path('check_in/<int:pk>', views.RegistrationCheckInUserView.as_view(), name='check_in'),
]