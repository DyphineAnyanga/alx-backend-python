from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access or modify it.
    Assumes the object has a 'user' or 'owner' attribute.
    """

    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user', None) == request.user or getattr(obj, 'owner', None) == request.user


class IsParticipantOfConversation(BasePermission):

    """
    Allow access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE", "GET", "POST"]:
            return request.user in obj.conversation.participants.all()
        return False


    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return request.user in [obj.sender, obj.receiver]
        return False
