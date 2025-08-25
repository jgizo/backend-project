from rest_framework import viewsets
from .models import ChatRoom, Message, Conversation
from .serializers import ChatRoomSerializer, MessageSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

@login_required
def chat_home(request):
    conversations = request.user.conversations.all()
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/chat_home.html", {"conversations": conversations, "users": users})

@login_required
def start_private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    conversation = Conversation.objects.filter(is_group=False, members=request.user).filter(members=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create(is_group=False)
        conversation.members.add(request.user, other_user)

    return redirect("chat_room", conversation_id=conversation.id)

@login_required
def create_group_chat(request):
    if request.method == "POST":
        name = request.POST.get("name")
        member_ids = request.POST.getlist("members")
        conversation = Conversation.objects.create(name=name, is_group=True)
        members_to_add = list(User.objects.filter(id__in=member_ids))
        conversation.members.add(request.user, *members_to_add)
        return redirect("chat_room", conversation_id=conversation.id)
    
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/create_group.html", {"users": users})

@login_required
def chat_room(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, members=request.user)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
    
    messages = conversation.messages.all().order_by("timestamp")
    return render(request, "messaging/chat_room.html", {"conversation": conversation, "messages": messages})
