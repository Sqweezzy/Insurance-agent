from rest_framework import serializers

from .models import Document


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'doc_type', 'file', 'uploaded_at']
        

class DocumentDetailDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_at']
        
    def validate(self, data):
        policy = self.instance.policy_id
        if policy.agent_id != self.context['request'].user:
            raise serializers.ValidationError("You can only access documents for your own policies.")        
        return data
        
    def delete(self):
        self.instance.file.delete(save=False)
        self.instance.delete()


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['policy_id', 'client_id', 'doc_type', 'file']
    
    def validate(self, data):
        policy = data.get('policy_id')
        client = data.get('client_id')
        if policy.client_id != client:
            raise serializers.ValidationError("The document must be associated with the correct client and policy.")
        if policy.agent_id != self.context['request'].user:
            raise serializers.ValidationError("You can only upload documents for your own policies.")
        return data

    def create(self, validated_data):
        document = Document.objects.create(**validated_data)
        return document
