from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts.views import PostViewSet
from apps.category.views import CategoryListView
from .views import HealthCheckView

router = DefaultRouter()
router.register(r'', PostViewSet, basename='')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('healthz/', HealthCheckView.as_view(), name='health-check'),

    path('api/', include([
        path('', include(router.urls)),
        path('categories/', CategoryListView.as_view(), name='category-list'),
    ])),
]