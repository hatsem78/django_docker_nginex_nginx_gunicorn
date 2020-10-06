from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'meetup_enroll_invite_users'

urlpatterns = [
    url('list/', views.MeetupEnrollInviteUsersAdd.as_view(), name='list'),
    url('list_page/', views.MeetupEnrollInviteUsersModuleList.as_view(), name='list_page'),
    path('create/', views.MeetupEnrollInviteUsersAdd.as_view(), name='create'),
    path('update/<int:pk>', views.MeetupEnrollInviteUsersModuleDetail.as_view(), name='update'),
    path('get_meetup_enroll_invite_users/<int:pk>', views.MeetupEnrollInviteUsersModuleDetail.as_view(), name='get_meetup_enroll_invite_users'),
    path('delete/<int:pk>', views.MeetupEnrollInviteUsersModuleDetail.as_view(), name='delete'),
    path('get_notification/<int:pk>', views.MeetupEnrollInviteUsersModuleDetail.as_view(), name='get_notification'),



]

