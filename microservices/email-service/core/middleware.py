import time
import json
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        
        # Esqueleto para leer el token JWT
        auth_header = request.headers.get("Authorization", None)
        
        log_data = {
            "path": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "response_time_ms": round(duration * 1000, 2),
            "authorization_header_present": bool(auth_header),
        }

        logger.info(json.dumps(log_data))

        return response

