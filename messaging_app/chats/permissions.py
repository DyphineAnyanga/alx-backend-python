from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes the object has a 'user' or 'owner' attribute linking to the user
        return getattr(obj, 'user', None) == request.user or getattr(obj, 'owner', None) == request.user

