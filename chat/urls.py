from django.urls import path
from .views import CreateChatAPI, ListMessageAPI,ListChatAPI, UpdateChatStatus, CreateMessageAPI


urlpatterns = [
    path('create_chat/', CreateChatAPI.as_view(),name='createChat'),
    path('list_chat/',ListChatAPI.as_view(),name='ListChat'),
    path('send-message/<int:id>/',CreateMessageAPI.as_view()),
    path('<int:id>/',ListMessageAPI.as_view(),name='createListMessages'),
    path('update-chat-status/<int:chat_id>/',UpdateChatStatus.as_view()),
]