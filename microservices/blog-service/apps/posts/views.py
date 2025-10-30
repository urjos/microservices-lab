import logging
import requests
import uuid
from django.conf import settings
from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from django.db.models import F
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer

logger = logging.getLogger(__name__)

class PostViewSet(mixins.CreateModelMixin, # ¡Añadimos este mixin para permitir la creación!
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    Un ViewSet para listar y ver detalles de Posts.
    - GET /api/posts/ -> Lista paginada de posts publicados.
    - GET /api/posts/?search=... -> Busca posts por título o cuerpo.
    - GET /api/posts/{slug}/ -> Muestra el detalle de un post.
    """
    queryset = Post.objects.filter(status='published').select_related('author', 'category')
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        if self.action == 'create': # Usar PostCreateSerializer para la acción de creación
            return PostCreateSerializer
        return PostListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
    # Comenta o elimina estas dos líneas:
    # if 'dispatch' in self._decorators:
    #     self._decorators['dispatch'] = []
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Guarda el nuevo post y luego, si está publicado, notifica al email-service.
        """
        post = serializer.save()
        logger.info(f"Nuevo post creado: {post.title} (ID: {post.id})")

        # Notificar al email-service solo si el post está publicado
        if post.status == 'published':
            self._send_new_post_notification(post)

    def _send_new_post_notification(self, post):
        """
        Envía una notificación al email-service sobre un nuevo post publicado.
        """
        notification_url = f"{settings.EMAIL_SERVICE_BASE_URL}/api/notify/"
        recipient_email = settings.BLOG_POST_NOTIFICATION_RECIPIENT
        subject = f"Nuevo Post Publicado: {post.title}"
        message_body = (
            f"Se ha publicado un nuevo post en el blog:\n\n"
            f"Título: {post.title}\n"
            f"Autor: {post.author.display_name}\n"
            f"Categoría: {post.category.name}\n"
            f"Puedes leerlo aquí: [Enlace al post, si tu frontend lo genera]\n\n" # ¡Importante! Reemplaza esto con la URL real de tu frontend
            f"Resumen: {post.body[:200]}..."
        )
        # Generamos una clave de idempotencia única para esta notificación
        idempotency_key = f"blog-post-notification-{post.id}-{uuid.uuid4()}"

        payload = {
            "to": recipient_email,
            "subject": subject,
            "body": message_body,
            "idempotency_key": idempotency_key
        }

        try:
            response = requests.post(notification_url, json=payload, timeout=5)
            response.raise_for_status() # Lanza una excepción para códigos de estado HTTP de error (4xx o 5xx)
            logger.info(f"Notificación para el post '{post.title}' enviada al email-service. Respuesta: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Fallo al enviar notificación para el post '{post.title}' al email-service: {e}")
        except Exception as e:
            logger.error(f"Ocurrió un error inesperado al notificar al email-service para el post '{post.title}': {e}")
