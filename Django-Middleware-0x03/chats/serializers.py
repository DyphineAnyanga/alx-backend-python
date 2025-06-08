from rest_framework import serializers
from .models import User, Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    message_summary = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at', 'created_at', 'message_summary']

    def get_message_summary(self, obj):
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'password']

    def validate_phone_number(self, value):
        if not value.startswith('+') or not value[1:].isdigit():
            raise serializers.ValidationError("Phone number must start with '+' followed by digits.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']

