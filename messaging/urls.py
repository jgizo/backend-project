from rest_framework.routers import DefaultRouter
from messaging.views import ChatRoomViewSet, MessageViewSet
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from .views import *

router = DefaultRouter()
router.register(r"chatrooms", ChatRoomViewSet)
router.register(r"messages", MessageViewSet)

urlpatterns = [ 
    path('home/', chat_home, name='chat_home'),
    path("private/<int:user_id>", start_private_chat, name="start_private_chat"),
    path("group/create/", create_group_chat, name="create_group_chat"),
    path("<int:conversation_id>/", chat_room, name="chat_room"),
]
