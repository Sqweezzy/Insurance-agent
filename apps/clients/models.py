from django.db import models
from apps.accounts.models import Agent

class Client(models.Model):
    agent_id = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='clients')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(blank=True, null=True)
    passport_series = models.CharField(max_length=4, blank=True, null=True)
    passport_number = models.CharField(max_length=6, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['agent_id', '-created_at']
        