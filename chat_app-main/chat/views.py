from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def base(request):
    users = User.objects.exclude(id=request.user.id)
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # Sort user_last_messages by the timestamp of the last_message in descending order
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else datetime.min.replace(tzinfo=timezone.utc),
        reverse=True
    )

    return render(request, 'chat.html', {
        'users': users,
        'user_last_messages': user_last_messages
    })

@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id) 
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # Sort user_last_messages by the timestamp of the last_message in descending order
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else datetime.min.replace(tzinfo=timezone.utc),
        reverse=True
    )

    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def frontend(request):
    return render(request, 'Frontend_Development.html')

@login_required
def delete_all_users(request):
    if request.method == 'POST':
        User.objects.all().delete()
        messages.success(request, 'All users have been deleted successfully.')
        return redirect('user_list')
    return render(request, 'confirm_delete.html')