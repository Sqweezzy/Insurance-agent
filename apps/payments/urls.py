from django.urls import include, path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('detail/<int:pk>/', views.PaymentDetailUpdateView.as_view(), name='payment-detail-update')
]