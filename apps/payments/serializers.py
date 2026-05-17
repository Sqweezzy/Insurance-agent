from rest_framework import serializers
from .models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'status', 'payment_method']
        

class PaymentDetailCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'amount', 'payment_method', 'transaction_id','payment_date', 'created_at']

    def validate(self, attrs):
        if self.instance and self.instance.status == 'completed' and attrs.get('status') != 'completed':
            raise serializers.ValidationError("Невозможно изменить статус завершенного платежа.")
        return attrs
    
    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        # Логика для создания платежа (например, интеграция с платежным шлюзом)
        return payment
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        # Логика для обновления платежа (например, уведомление клиента)
        return instance
