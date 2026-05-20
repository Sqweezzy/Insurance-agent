from rest_framework import serializers
from .models import InsuranceType, Policy
from ..clients.models import Client
from ..accounts.models import Agent

class InsuranceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceType
        fields = ['id', 'name', 'code', 'description']


class PolicyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'policy_number', 'client_id', 'insurance_type', 'status', 'end_date']


class PolicyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'


class PolicyCreateSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    insurance_type = serializers.PrimaryKeyRelatedField(queryset=InsuranceType.objects.all())

    class Meta:
        model = Policy
        fields = ['client_id', 'insurance_type', 'policy_number', 'start_date', 'end_date',
                  'insurance_sum', 'premium', 'commission_rate', 'status', 'notes']

    def validate(self, data):
        if data['client_id'].agent_id != self.context['request'].user:
            raise serializers.ValidationError("Client must belong to the authenticated user.")
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        if Policy.objects.filter(policy_number=data['policy_number']).exists():
            raise serializers.ValidationError("Policy number must be unique.")
        return data

    def create(self, validated_data):
        validated_data['agent_id'] = self.context['request'].user
        return super().create(validated_data)


class PolicyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Policy
        fields = ['client_id', 'insurance_type', 'policy_number', 'start_date', 'end_date',
                  'insurance_sum', 'premium', 'commission_rate', 'status', 'notes']
        
    def validate(self, data):
        client = data.get('client_id', self.instance.client_id)
        if client.agent_id != self.context['request'].user:
            raise serializers.ValidationError("Client must belong to the authenticated user.") 
        if 'start_date' in data and 'end_date' in data:
            if data['end_date'] <= data['start_date']:
                raise serializers.ValidationError("End date must be after start date.")
        if 'policy_number' in data:
            if Policy.objects.filter(policy_number=data['policy_number']).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Policy number must be unique.")
        return data
    
    def update(self, instance, validated_data):
        validated_data['agent'] = self.context['request'].user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
