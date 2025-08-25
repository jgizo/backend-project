from django.contrib import admin
from .models import ChatRoom, Message
from django.utils import timezone

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "room_type")
    filter_horizontal = ("members",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipient", "room", "content", "timestamp_est")
    list_filter = ("room", "sender", "recipient")
    search_fields = ("content", "sender__username", "recipient__username")

    def timestamp_est(self, obj):
        return timezone.localtime(obj.timestamp).strftime("%Y-%m-%d %I:%M %p")
    
    timestamp_est.short_description = "Timestamp (EST)"