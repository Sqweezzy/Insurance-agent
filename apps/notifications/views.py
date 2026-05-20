from functools import partial
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Notification
from .serializers import (
    NotificationListSerializer,
    NotificationDetailSerializer,
    NotificationMarkReadSerializer
)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = request.user.notifications.all().order_by('-created_at')
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            notification = request.user.notifications.get(pk=pk)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NotificationDetailSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = request.user.notifications.get(pk=pk)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NotificationMarkReadSerializer(notification, data=request.data, context={'request': request})
        serializer.update(notification, {})

        return Response(
            {"detail": "Notification marked as read."},
            status=status.HTTP_200_OK
        )
