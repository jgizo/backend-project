from django.db import models
from django.conf import settings

class Conversation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    is_group = models.BooleanField(default=False)

    def __str__(self):
        if self.is_group:
            return self.name or f"Group {self.id}"
        else:
            return "Private chat: " + ", ".join([p.username for p in self.participants.all()])

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, 
                                  blank=True, related_name="received_messages")

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey("ChatRoom", on_delete=models.CASCADE, null=True, blank=True, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        if self.room:
            return f"[Room: {self.room}] {self.sender} messaged {self.recipient} at {self.timestamp}: {self.content}"
        else:
            return f"{self.sender} messaged {self.recipient} at {self.timestamp}: {self.content}"
    
class ChatRoom(models.Model):
    ROOM_TYPES = [
        ("private", "Private"),
        ("group", "Group"),
    ]

    name = models.CharField(max_length=255, blank=True, null=True)
    room_type = models.CharField(max_length=7, choices=ROOM_TYPES, default="private")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chatrooms")

    def __str__(self):
        return self.name or f"Room {self.id}"
    
