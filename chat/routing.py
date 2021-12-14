from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', consumers.Send_Message.as_asgi()),
]