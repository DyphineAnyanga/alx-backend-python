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
    Optimized using `.only()` to retrieve only necessary fields.
    """
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'created_at')
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages
    })


@login_required
def sent_messages_view(request):
    """
    Show messages sent by the logged-in user.
    Optimized with .only().
    """
    sent_messages = Message.objects.filter(sender=request.user).only('id', 'receiver', 'content', 'created_at')
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
    View message details. Mark the message as read if the user is the receiver.
    """
    message = get_object_or_404(Message, id=message_id)

    # Only mark as read if the logged-in user is the receiver
    if message.receiver == request.user and not message.read:
        message.read = True
        message.save()

    return render(request, 'messaging/message_detail.html', {
        'message': message
    })
