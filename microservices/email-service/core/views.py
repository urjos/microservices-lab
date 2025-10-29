import logging
from django.core.cache import caches
from django.db import connections
from django.db.utils import OperationalError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        # Verificar conexión a la base de datos
        db_conn = connections['default']
        try:
            db_conn.cursor()
        except OperationalError:
            return Response({"database": "error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Verificar conexión a Redis
        try:
            caches['default'].get('healthz')
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return Response({"redis": "error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({"status": "ok"}, status=status.HTTP_200_OK)
