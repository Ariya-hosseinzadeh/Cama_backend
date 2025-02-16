from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    User = get_user_model()
    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(user1=user) | Q(user2=user))

    def perform_create(self, serializer):
        user1 = self.request.user
        user2_id = self.request.data.get("user2")
        if not user2_id:
            raise serializer.ValidationError("User2 is required.")
        user2 = self.User.objects.get(id=user2_id)
        chat, created = Chat.objects.get_or_create(user1=user1, user2=user2)
        serializer.instance = chat

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat = Chat.objects.get(id=self.request.data.get("chat"))
        serializer.save(sender=self.request.user, chat=chat)
