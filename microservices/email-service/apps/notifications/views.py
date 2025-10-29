import logging
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Simulación de envío de correo (se mostrará en la consola de Docker)
        data = serializer.validated_data
        logger.info(f"Simulating email sending for contact message: {data['email']}")
        send_mail(
            subject=f"New contact message from {data['name']}",
            message=data['message'],
            from_email="noreply@solopython.com", # Remitente genérico
            recipient_list=[data['email']], # En un caso real, sería a un admin
            fail_silently=False,
        )

        return Response({"status": "queued"}, status=status.HTTP_201_CREATED)

