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
    Display unread messages for the logged-in user.
    Uses `Message.objects.filter()` for clarity.
    Optimized with `.select_related()` and `.only()`.
    """
    unread_messages = (
        Message.objects
        .filter(receiver=request.user, read=False)
        .select_related('sender')
        .only('id', 'sender__username', 'content', 'created_at')
    )
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages
    })


@login_required
def sent_messages_view(request):
    """
    Show messages sent by the logged-in user.
    Uses `Message.objects.filter()` explicitly.
    Optimized with `.select_related()` and `.only()`.
    """
    sent_messages = (
        Message.objects
        .filter(sender=request.user)
        .select_related('receiver')
        .only('id', 'receiver__username', 'content', 'created_at')
    )
    return render(request, 'messaging/sent.html', {
        'sent_messages': sent_messages
    })


@login_required
def send_message_view(request):
    """
    Allow the user to send a new message.
    """
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messaging:sent_messages')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})


@login_required
def message_detail_view(request, message_id):
    """
    View message details.
    If the logged-in user is the receiver and the message is unread, mark it as read.
    Optimized with `.select_related()` for sender and receiver.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver'),
        id=message_id
    )

    if message.receiver == request.user and not message.read:
        message.read = True
        message.save()

    return render(request, 'messaging/message_detail.html', {
        'message': message
    })
