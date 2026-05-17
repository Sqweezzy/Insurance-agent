from rest_framework import serializers
from .models import Client

class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'patronymic', 'phone', 'is_archived']


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'patronymic', 'phone', 'email', 'birth_date', 'passport_series',
                  'passport_number', 'address']
    
    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError('A client with this email already exists.')
        return value

    def create(self, validated_data):
        validated_data['agent_id'] = self.context['request'].user
        client = Client.objects.create(**validated_data)
        return client


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'patronymic', 'phone', 'email', 'birth_date', 'passport_series',
                  'passport_number', 'address', 'is_archived']
    
    def validate_email(self, value):
        client_id = self.instance.id
        if Client.objects.filter(email=value).exclude(id=client_id).exists():
            raise serializers.ValidationError('A client with this email already exists.')
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ClientArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['is_archived']
    
    def validate(self, attrs):
        client_id = self.instance.id
        if Client.objects.filter(id=client_id, is_archived=True).exists():
            raise serializers.ValidationError('This client is already archived.')
        return attrs
    
    def update(self, instance, validated_data):
        instance.is_archived = True
        instance.save()
        return instance
    