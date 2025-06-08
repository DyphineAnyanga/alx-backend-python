from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']  # or any field you want searchable

    def create(self, request, *args, **kwargs):
        """
        Override create to handle creating conversations with participants.
        Expecting a list of user IDs in the request data.
        """
        participants = request.data.get('participants', [])
        if not participants or not isinstance(participants, list):
            return Response({"error": "Participants list is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the conversation with participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create to handle sending a message to a conversation.
        Expect conversation ID and message body in the request.
        """
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        sender = request.user

        if not conversation_id or not message_body:
            return Response({"error": "conversation and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verify conversation exists
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Optionally check if sender is part of the conversation
        if sender not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
