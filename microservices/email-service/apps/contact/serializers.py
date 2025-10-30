from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    idempotency_key = serializers.UUIDField(write_only=True)

    class Meta:
        model = ContactMessage
        fields = [
            'name',
            'email',
            'message',
            'idempotency_key' 
        ]