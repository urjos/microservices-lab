from rest_framework import viewsets, mixins, filters
from rest_framework.response import Response
from django.db.models import F
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer


class PostViewSet(mixins.ListModelMixin,
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