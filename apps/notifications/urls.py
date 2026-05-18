from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('detail/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('mark-read/<int:pk>/', views.NotificationMarkReadView.as_view(), name='notification-mark-read'),
]
