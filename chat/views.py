from django.db.models import Q
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateChatSerializer, MessageSerializer,ChatListSerializer
from .permissions import IsAdvisor
from .models import Message,Chat_User,Chat

# Create your views here.


class CreateChatAPI(generics.CreateAPIView):
    serializer_class = CreateChatSerializer
    permission_classes = [IsAuthenticated,IsAdvisor]


class ListChatAPI(generics.ListAPIView):
    serializer_class = ChatListSerializer

    def get_queryset(self):
        chats = Chat.objects.filter(chats_users__user=self.request.user)
        chat_users = Chat_User.objects.filter(Q(chat__in=chats))
        return chat_users.exclude(user_id=self.request.user.id).order_by('-chat__time_changed')


class CreateListMessageAPI(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(Q(chat_id=self.kwargs.get('id'))).order_by('-date')