from django.contrib import admin

from .models import InsuranceType, Policy


@admin.register(InsuranceType)
class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_number', 'client_id', 'insurance_type', 'status', 'end_date')
    search_fields = ('policy_number', 'client_id__name', 'insurance_type__name')
    list_filter = ('status', 'insurance_type')
    
    