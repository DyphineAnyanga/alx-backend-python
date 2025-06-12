from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm


@login_required
def inbox_view(request):
    """
    Display only unread messages for the logged-in user.
    Optimized using `.only()` to retrieve essential fields only.
    """
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages
    })


@login_required
def send_message(request, username=None, parent_id=None):
    """
    Send a message to a user. If replying, link to the parent message.
    """
    recipient = get_object_or_404(User, username=username) if username else None
    parent_message = get_object_or_404(Message, id=parent_id) if parent_id else None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.parent_message = parent_message
            message.save()
            return redirect('inbox')  # Or redirect to message thread
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {
        'form': form,
        'recipient': recipient,
        'parent_message': parent_message
    })


@login_required
def thread_view(request, message_id):
    """
    Display a message and all its recursive replies in a threaded view.
    Optimized with `select_related` and `prefetch_related`.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                       .prefetch_related('replies'),
        id=message_id
    )

    def get_replies(msg):
        # Recursive function to gather all threaded replies
        replies = msg.replies.select_related('sender', 'receiver').all()
        all_replies = []
        for reply in replies:
            all_replies.append(reply)
            all_replies.extend(get_replies(reply))
        return all_replies

    threaded_replies = get_replies(message)

    return render(request, 'messaging/thread.html', {
        'message': message,
        'threaded_replies': threaded_replies
    })
