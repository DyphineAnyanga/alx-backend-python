from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message, Conversation

@cache_page(60)
@login_required
def conversation_messages_view(request, conversation_id):
    """
    Display messages for a specific conversation.
    This view is cached for 60 seconds to reduce database load.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in [conversation.sender, conversation.receiver]:
        return render(request, '403.html', status=403)

    messages = (
        Message.objects
        .filter(conversation=conversation)
        .select_related('sender', 'receiver')
        .only('id', 'sender__username', 'receiver__username', 'content', 'created_at')
        .order_by('created_at')
    )

    return render(request, 'chats/conversation_messages.html', {
        'conversation': conversation,
        'messages': messages
    })
