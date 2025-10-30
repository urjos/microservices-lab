import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3},
    retry_backoff=True,
    retry_backoff_max=60
)
def send_email_task(subject, message, recipient_list):
    """
    Tarea de Celery para enviar un correo electrónico de forma asíncrona.
    """
    logger.info(f"Sending email to {recipient_list} with subject: '{subject}'")
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@solopython.com')

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    logger.info("Email sent successfully.")