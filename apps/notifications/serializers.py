from time import timezone

from rest_framework import serializers

from .models import Notification


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['type', 'message', 'created_at', 'is_read']


class NotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'agent_id', 'policy_id', 'type', 'message', 'created_at']


class NotificationMarkReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read', 'read_at']
    
    def validate(self, data):
        if self.instance.is_read == True:
            raise serializers.ValidationError("This notification is already marked as read.")
        if self.instance.agent_id != self.context['request'].user:
            raise serializers.ValidationError("You can only mark your own notifications as read.")
        return data

    def update(self, instance, validated_data):
        instance.is_read = True
        instance.read_at = timezone.now()
        instance.save()
        return instance
    