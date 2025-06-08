# 0x03-MessagingApp-Django/chats/middleware.py

from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict
import threading


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.lock = threading.Lock()

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with self.lock:
            with open("requests.log", "a") as f:
                f.write(log_line)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Chat allowed only between 6 AM (6) and 9 PM (21)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access denied: Chatting allowed only between 6 AM and 9 PM.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    message_log = defaultdict(list)
    lock = threading.Lock()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            with self.lock:
                # Clear timestamps older than 1 minute
                self.message_log[ip] = [t for t in self.message_log[ip] if now - t < timedelta(minutes=1)]

                if len(self.message_log[ip]) >= 5:
                    return HttpResponseForbidden("Message limit exceeded: Max 5 messages per minute allowed.")

                self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        # Ensure user is authenticated and role is admin or moderator
        if not user.is_authenticated or getattr(user, "role", None) not in ["admin", "moderator"]:
            return HttpResponseForbidden("Access denied: Insufficient permissions.")
        return self.get_response(request)
