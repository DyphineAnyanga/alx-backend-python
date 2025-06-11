from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User

def get_threaded_replies(message):
    """
    Recursively fetch all replies to a given message.
    """
    replies = message.replies.select_related('sender', 'receiver').all()
    all_replies = []
    for reply in replies:
        all_replies.append(reply)
        all_replies.extend(get_threaded_replies(reply))
    return all_replies

@login_required
def conversation_view(request, receiver_id):
    """
    Fetch messages between request.user and receiver, along with threaded replies.
    Optimized with select_related and prefetch_related.
    """
    receiver = get_object_or_404(User, id=receiver_id)

    # Main messages
    messages = Message.objects.filter(
        sender=request.user,
        receiver=receiver,
        parent_message=None
    ).select_related('sender', 'receiver').prefetch_related('replies')

    # Append all replies recursively for UI rendering
    message_threads = []
    for msg in messages:
        thread = {
            'message': msg,
            'replies': get_threaded_replies(msg)
        }
        message_threads.append(thread)

    return render(request, 'messaging/conversation.html', {
        'receiver': receiver,
        'message_threads': message_threads
    })
