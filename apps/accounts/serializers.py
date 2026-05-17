from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Agent


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Agent
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone', 'license_number', 'company']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Password confirmation does not match password.'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Agent.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        
        login = attrs['login']
        password = attrs['password']

        user = authenticate(
            request=self.context.get('request'),
            username=login,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError('Invalid login or password.')
        
        attrs['user'] = user
        return attrs


class AgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'license_number', 'company']
        


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'New password confirmation does not match new password.'})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    