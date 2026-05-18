from django.db import models

from apps.clients.models import Client
from apps.policies.models import Policy

class Document(models.Model):
    policy_id = models.ForeignKey(Policy, on_delete=models.PROTECT, related_name='documents')
    client_id = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='documents')
    doc_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.doc_type} for {self.policy_id.policy_number}"
    
    
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['policy_id', '-uploaded_at']
        