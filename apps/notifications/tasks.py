from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ..policies.models import Policy
from .models import Notification


@shared_task
def check_expiring_policies():
    today = timezone.now().date()

    for days in [30, 7, 1]:
        expiring = Policy.objects.filter(
            end_date=today + timedelta(days=days),
            status='active'
        )
        
        for policy in expiring:
            already_exists = Notification.objects.filter(
                policy_id=policy,
                type='expiring',
                message__contains=f'{days} дн'
            ).exists()
            
            if not already_exists:
                Notification.objects.create(
                    agent_id=policy.agent_id,
                    policy_id=policy,
                    type='expiring',
                    message=f'Полис {policy.policy_number} истекает через {days} дн. ({policy.end_date})'
                )
                