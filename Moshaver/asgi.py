"""
ASGI config for Moshaver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Moshaver.settings')

# application = get_asgi_application()


# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })


# import os

# import django
# from channels.http import AsgiHandler
# from channels.routing import ProtocolTypeRouter

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# django.setup()

# application = ProtocolTypeRouter({
#   "http": AsgiHandler(),
#   # Just HTTP for now. (We can add other protocols later.)
# })


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing
from django.urls import path
from chat.consumers import Send_Message
from login.consumers import RequestConsumer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Moshaver.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": 
        URLRouter([
            path('ws/chat/<int:chat_id>/<str:token>/', Send_Message.as_asgi()),
            path('ws/user/request/<str:advisor_id>/<str:request_content>', RequestConsumer.as_asgi()),
            path('ws/advisor/request/<str:request_id>/<int:answer>', RequestConsumer.as_asgi()),
        ]),
    
})


# import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.conf.urls import url
# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Moshaver.settings")
# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()

# from chat.consumers import Send_Message

# application = ProtocolTypeRouter({
#     # Django's ASGI application to handle traditional HTTP requests
#     "http": django_asgi_app,

#     # WebSocket chat handler
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             url(r"^chat/admin/$", Send_Message.as_asgi())
#         ])
#     ),
# })