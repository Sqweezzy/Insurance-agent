from django.db import models
from ..policies.models import Policy


class Payment(models.Model):
    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Payment {self.id} for Policy {self.policy_id}'
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']
        