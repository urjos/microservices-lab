from apps.category.serializers import CategorySerializer
from rest_framework import generics
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Category


@method_decorator(cache_page(120), name='get')
class CategoryListView(generics.ListAPIView):
    """
    - GET /api/categories/ -> Lista todas las categorías activas.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None # No paginar categorías