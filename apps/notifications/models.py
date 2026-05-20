from django.db import models

from apps.accounts.models import Agent
from apps.policies.models import Policy


class Notification(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='notifications')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    type = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return f"Notification for {self.agent_id} - {self.type}"
    
    class Meta:
        verbose_name = 'Notifications'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['agent_id', 'is_read']),
        ]
