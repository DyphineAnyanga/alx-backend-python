from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('sent/', views.sent_messages_view, name='sent_messages'),
    path('send/', views.send_message_view, name='send_message'),
    path('message/<int:message_id>/', views.message_detail_view, name='message_detail'),
]
