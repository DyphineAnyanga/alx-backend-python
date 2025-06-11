from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message

@login_required
def threaded_conversations(request):
    """
    View to display threaded messages between the logged-in user and others.
    Messages include replies (parent_message) and are optimized with select_related and prefetch_related.
    """
    user = request.user
    messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user),
        parent_message__isnull=True  # Only top-level messages (not replies)
    ).select_related('sender', 'receiver', 'parent_message')\
     .prefetch_related('replies')

    context = {
        'messages': messages
    }
    return render(request, 'messaging/threaded.html', context)

@login_required
def delete_user(request):
    """
    View to allow a user to delete their account.
    """
    user = request.user
    if request.method == "POST":
        user.delete()
        return render(request, 'messaging/account_deleted.html')
    return render(request, 'messaging/confirm_delete.html')
