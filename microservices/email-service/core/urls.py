from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HealthCheckView
from apps.notifications.views import NotifyViewSet
from apps.contact.views import ContactMessageViewSet

router = DefaultRouter()
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'notify', NotifyViewSet, basename='notify')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('healthz/', HealthCheckView.as_view(), name='health-check'),

    path('api/', include(router.urls)),
]
