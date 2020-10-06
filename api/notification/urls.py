from django.urls import path

from . import views

app_name = 'notification'

urlpatterns = [
    path('list/', views.NotificationAdd.as_view(), name='list'),
    path('list_page/', views.NotificationModuleList.as_view(), name='list_page'),
    path('create/', views.NotificationAdd.as_view(), name='create'),
    path('update/<int:pk>', views.NotificationModuleDetail.as_view(), name='update'),
    path('delete/<int:pk>', views.NotificationModuleDetail.as_view(), name='delete'),
    path('is_seen/<int:pk>', views.NotificationSeenReadDetail.as_view(), name='is_seen'),
    path('is_read/<int:pk>', views.NotificationSeenReadDetail.as_view(), name='is_read'),

]