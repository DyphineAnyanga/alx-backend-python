from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from chat.views import UserViewSet, MessageViewSet
from chats.views import ConversationViewSet, MessageViewSet as ConversationMessageViewSet

# Main router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested messages under users
user_router = NestedDefaultRouter(router, r'users', lookup='user')
user_router.register(r'messages', MessageViewSet, basename='user-messages')

# Nested messages under conversations
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', ConversationMessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(user_router.urls)),
    path('api/', include(conversation_router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # browsable API login
]

