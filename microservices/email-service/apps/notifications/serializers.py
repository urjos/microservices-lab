from rest_framework import serializers
from .models import NotificationLog

class NotificationLogSerializer(serializers.ModelSerializer):
    idempotency_key = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = NotificationLog
        fields = ['to', 'subject', 'body', 'idempotency_key']