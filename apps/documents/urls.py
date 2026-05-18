from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.DocumentListCreateView.as_view(), name='document-list'),
    path('detail/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
]
