from django.urls import path

from . import views

app_name = 'meetup'

urlpatterns = [
    path('list/', views.MeetupAdd.as_view(), name='list'),
    path('list_page/', views.MeetupModuleList.as_view(), name='list_page'),
    path('create/', views.MeetupAdd.as_view(), name='create'),
    path('update/<int:pk>', views.MeetupModuleDetail.as_view(), name='update'),
    path('get_meetup/<int:pk>', views.MeetupModuleDetail.as_view(), name='get_meetup'),
    path('delete/<int:pk>', views.MeetupModuleDetail.as_view(), name='delete'),

]