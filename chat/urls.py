from django.urls import path
from .views import CreateChatAPI,CreateListMessageAPI,ListChatAPI

urlpatterns = [

    path('create_chat/',CreateChatAPI.as_view(),name='createChat'),
    path('list_chat/',ListChatAPI.as_view(),name='ListChat'),
    path('<int:id>/',CreateListMessageAPI.as_view(),name='createListMessages')
]