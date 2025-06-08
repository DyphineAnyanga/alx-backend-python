from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(conversation__id=conversation_id, conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation."},
                           status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)

