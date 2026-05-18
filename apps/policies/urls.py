from django.urls import path
from . import views

app_name = 'policies'

urlpatterns = [
    path('', views.PolicyListCreateView.as_view(), name='policy-list-create'),
    path('detail/<int:pk>/', views.PolicyDetailUpdateView.as_view(), name='policy-detail'),
    path('insurance-types/', views.InsuranceTypeListView.as_view(), name='insurance-type-list'),
]