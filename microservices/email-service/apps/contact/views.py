import logging
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from apps.notifications.tasks import send_email_task

logger = logging.getLogger(__name__)

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        request_data = request.data
        idempotency_key = request_data.get('idempotency_key') # <-- Usa .get()

        if not idempotency_key:
            return Response({"error": "Idempotency key is required."}, status=status.HTTP_400_BAD_REQUEST)

        if cache.get(idempotency_key):
            logger.warning(f"Duplicate request detected with idempotency key: {idempotency_key}")
            return Response({"status": "already_processed"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request_data)

        serializer.is_valid(raise_exception=True)

        cache.set(idempotency_key, 'processing', timeout=60*60*24)

        self.perform_create(serializer)

        data_for_task = serializer.validated_data.copy()
        logger.info(f"Queueing contact email to: {data_for_task['email']}")
        send_email_task.delay(
            subject=f"New contact message from {data_for_task['name']}",
            message=data_for_task['message'],
            recipient_list=[data_for_task['email']]
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Saca la idempotency_key antes de guardar."""
        validated_data = serializer.validated_data
        validated_data.pop('idempotency_key', None)
        serializer.save()