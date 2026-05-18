from django.contrib import admin
from .models import Agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at',)
    
    