from django.db.models import Q
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CreateChatSerializer, MessageSerializer,ChatListSerializer, ChatUserSerializer
from .permissions import IsAdvisor, IsChatGetStarted, IsChatDone, IsChatFinishedAccordingToTime
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


class ListMessageAPI(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(Q(chat_id=self.kwargs.get('id'))).order_by('-date')


class CreateMessageAPI(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsChatGetStarted, IsChatDone, IsChatFinishedAccordingToTime]


class UpdateChatStatus(APIView):
    permission_classes = [IsAuthenticated, IsAdvisor ]
    def put(self, request, *args, **kwargs):
        Chat_User.objects.filter(chat= self.kwargs['chat_id']).update(is_done=True)

        return Response(status.HTTP_200_OK)