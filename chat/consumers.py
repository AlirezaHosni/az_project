import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Chat_User, Message, Chat
from login.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone


class Send_Message(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.objects.filter(chat=self.scope['url_route']['kwargs']['chat_id'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user_contact = self.user_id
        if self.has_permission_is_chat_get_started(self.user_id, self.chat_id) & self.has_permission_is_chat_done(self.user_id, self.chat_id) & self.has_permission_according_to_end_session_datetime(self.user_id, self.chat_id):
            message = Message.objects.create(
            user_id=user_contact,
            chat_id=self.scope['url_route']['kwargs']['chat_id'],
            text=data['text'])
        else:
            return {
                "error": "امکان ارسال پیام وجود ندارد"
            }

        # current_chat = get_current_chat(data['chatId'])
        # current_chat.messages.add(message)
        # current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'text': message.text,
            'date': str(message.date),
            'chat_id': message.chat_id,
            'user_id': message.user_id,
            'contact_user_status': self.get_user_status(self.user_id)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.chat_id = int(self.scope['url_route']['kwargs']['chat_id'])
        self.room_group_name = Chat.objects.get(pk=self.chat_id).title
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        try:
            token = self.scope['url_route']['kwargs']['token']
            self.user_id = Token.objects.get(key=token).user_id
            self.update_user_status(self.user_id, 'online')    
            self.accept()
        except(Token.DoesNotExist):
            return {
                "error": "این کاربر ناشناخته هست. ابتدا  وارد سایت شوید"
            }
        
        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.update_user_status(self.user_id, 'offline')

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def update_user_status(self, user_id, status):
        return User.objects.filter(pk=user_id).update(status=status)

    def get_user_status(self, user_id):
        return User.objects.get(pk=user_id).status

    def has_permission_according_to_end_session_datetime(self, user_id, chat_id):
        try:
            chat_user = Chat_User.objects.filter(user=user_id, chat=chat_id).first()
        except(Chat_User.DoesNotExist):
            return False
        
        if timezone.now() >= chat_user.end_session_datetime:
            return False
        return True

    def has_permission_is_chat_get_started(self, user_id, chat_id):
        try:
            chat_user = Chat_User.objects.filter(user=user_id, chat=chat_id).first()
        except(Chat_User.DoesNotExist):
            return False
        
        if timezone.now() < chat_user.chat_start_datetime:
            return False
        return True

    def has_permission_is_chat_done(self, user_id, chat_id):
        try:
            chat_user = Chat_User.objects.filter(user=user_id, chat=chat_id).first()
            if(chat_user.is_done == True):
                return False
        except(Chat_User.DoesNotExist):
            return False

        return True



# class Send_Message(WebsocketConsumer):
#     async def websocket_connect(self, event):
#         print("connected", event)
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#         self.room_group_name = self.get_chat_title()

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     async def websocket_disconnect(self, event):
#         # Leave room group
#         print("disconnected", event)
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     @database_sync_to_async
#     def get_chat_title(self):
#         return Chat.objects.get(pk=self.chat_id).title

#     @database_sync_to_async
#     def set_chat_message(self, text, chat_id, user_id):
#         return Message.objects.create(
#             text= text,
#             chat= chat_id,
#             user= user_id
#         )

#     # Receive message from WebSocket
#     async def websocket_receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         user_id = self.scope['user'].id
#         self.set_chat_message(message, self.chat_id, user_id)
        
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     #Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))

    