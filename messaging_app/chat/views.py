from rest_framework import viewsets
from .models import User, Message
from .serializers import UserSerializer, UserMessageSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk')
        return Message.objects.filter(sender_id=user_id)
