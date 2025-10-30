# email-service/apps/notifications/views.py
import logging
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import NotificationLog
from .serializers import NotificationLogSerializer
from .tasks import send_email_task # Asumiendo que tasks.py está un nivel arriba

logger = logging.getLogger(__name__)

class NotifyViewSet(viewsets.ModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        request_data = request.data
        idempotency_key = request_data.get('idempotency_key')

        if idempotency_key:
            if cache.get(idempotency_key):
                logger.warning(f"Duplicate notification request detected with idempotency key: {idempotency_key}")
                return Response({"status": "already_processed"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        if idempotency_key:
            cache.set(idempotency_key, 'processing', timeout=60*60*24)

        self.perform_create(serializer)

        data = serializer.validated_data # OJO: data ya no tendrá idempotency_key aquí
        logger.info(f"Queueing internal notification to: {data['to']}. Idempotency key checked: {idempotency_key}") # Loguea la clave original
        send_email_task.delay(
            subject=data['subject'],
            message=data['body'],
            recipient_list=[data['to']]
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Saca la idempotency_key antes de guardar."""
        validated_data = serializer.validated_data
        validated_data.pop('idempotency_key', None)
        serializer.save() 