import logging
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user info, fallback to 'Anonymous' if not authenticated
        user = request.user.username if hasattr(request.user, 'is_authenticated') and request.user.is_authenticated else 'Anonymous'

        # Log timestamp, user, and request path
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        return self.get_response(request)
from datetime import datetime, time
from django.http import HttpResponseForbidden

class TimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = time(21, 0)  # 9 PM
        end_time = time(6, 0)     # 6 AM

        # Deny access if current time is NOT between 9 PM and 6 AM
        # Since time spans across midnight, check accordingly:
        if current_time < start_time and current_time > end_time:
            return HttpResponseForbidden("Access denied: outside allowed access hours (9 PM - 6 AM).")

        return self.get_response(request)
import time
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = {}  # {ip: [(timestamp1), (timestamp2), ...]}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chat'):
            ip = self.get_client_ip(request)
            now = time.time()

            if ip not in self.request_log:
                self.request_log[ip] = []

            # Filter requests within the last 60 seconds
            one_minute_ago = now - 60
            self.request_log[ip] = [ts for ts in self.request_log[ip] if ts > one_minute_ago]

            if len(self.request_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            self.request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
from django.http import JsonResponse

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to protected admin/moderator routes
        protected_paths = ['/chat/delete', '/chat/moderate', '/admin-action']  # example routes

        if any(request.path.startswith(path) for path in protected_paths):
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=403)

            # Check if user has appropriate role
            if not (user.is_superuser or user.groups.filter(name__in=['admin', 'moderator']).exists()):
                return JsonResponse({'error': 'Access denied. Admin or Moderator required.'}, status=403)

        return self.get_response(request)
