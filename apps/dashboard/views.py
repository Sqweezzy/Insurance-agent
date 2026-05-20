# dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from ..policies.models import Policy
from ..clients.models import Client
from ..notifications.models import Notification
from ..payments.models import Payment


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agent = request.user
        today = timezone.now().date()
        month_start = today.replace(day=1)

        active_policies = Policy.objects.filter(
            agent_id=agent, status='active'
        ).count()
        
        expiring_soon = Policy.objects.filter(
            agent_id=agent,
            status='active',
            end_date__lte=today + timedelta(days=30),
            end_date__gte=today
        ).count()

        total_clients = Client.objects.filter(
            agent_id=agent, is_archived=False
        ).count()

        new_clients = Client.objects.filter(
            agent_id=agent,
            created_at__gte=month_start
        ).count()

        from django.db.models import Sum, F, ExpressionWrapper, DecimalField
        commission = Payment.objects.filter(
            policy_id__agent_id=agent,
            payment_date__gte=month_start,
            status='completed'
        ).aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('amount') * F('policy_id__commission_rate') / 100,
                    output_field=DecimalField()
                )
            )
        )['total'] or 0


        unread_notifications = Notification.objects.filter(
            agent_id=agent, is_read=False
        ).count()

        return Response({
            'active_policies': active_policies,
            'expiring_soon': expiring_soon,
            'total_clients': total_clients,
            'new_clients_this_month': new_clients,
            'commission_this_month': commission,
            'unread_notifications': unread_notifications,
        })
        