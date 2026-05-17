from django.db import models
from django.contrib.auth.models import AbstractUser

class Agent(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'
    
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
        ordering = ['-created_at']
        