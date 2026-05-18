from rest_framework import serializers
from .models import Payment
from ..policies.models import Policy


class PaymentListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['policy_id', 'amount', 'payment_date', 'status', 'payment_method']
        
    def validate(self, data):
        policy = data.get('policy_id')
        if policy.agent_id != self.context['request'].user:
            raise serializers.ValidationError("You can only create payments for your own policies.")
        return data
    
            
    def create(self, validated_data):
        print(validated_data)
        payment = Payment.objects.create(**validated_data)
        # Логика для создания платежа (например, интеграция с платежным шлюзом)
        return payment
        

class PaymentDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['policy_id', 'amount', 'payment_method', 'transaction_id','payment_date', 'created_at']

    def validate(self, attrs):
        policy = self.instance.policy_id
        if policy.agent_id != self.context['request'].user:
            raise serializers.ValidationError("You can only update payments for your own policies.")
        if self.instance and self.instance.status == 'completed' and attrs.get('status') != 'completed':
            raise serializers.ValidationError("You cannot change the status of a completed payment.")
        return attrs
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        # Логика для обновления платежа (например, уведомление клиента)
        return instance
