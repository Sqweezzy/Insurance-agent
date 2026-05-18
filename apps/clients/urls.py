from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientListCreateView.as_view(), name='client-list'),
    path('detail/<int:pk>/', views.ClientDetailUpdateView.as_view(), name='client-detail'),
    path('detail/<int:pk>/archive/', views.ClientArchiveView.as_view(), name='client-archive'),
    path('all/', views.ClientListViewALL.as_view(), name='client-list-all'),
]
