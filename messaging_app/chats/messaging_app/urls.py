from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # ✅ Required for routing to conversations/messages APIs
    path('api-auth/', include('rest_framework.urls')),  # ✅ Required for browsable API login/logout
]
