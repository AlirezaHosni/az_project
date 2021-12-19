from django.conf.urls import url
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('ws/chat/<int:chat_id>/', consumers.Send_Message.as_asgi()),
    # url(r'^ws/chat/(?P<chat_id>[^/]+)/$', consumers.Send_Message.as_asgi())
]