from django.db import models
from ..clients.models import Client
from ..accounts.models import Agent

class InsuranceType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Insurance Type"
        verbose_name_plural = "Insurance Types"


class Policy(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='policies')
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='policies')
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.PROTECT, related_name='policies')
    policy_number = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    insurance_sum = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('cancelled', 'Cancelled')], default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.policy_number} - {self.client_id.name}"
    
    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
        ordering = ['-created_at']
        