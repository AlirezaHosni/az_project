import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import channels.layers

from rest_framework.generics import get_object_or_404
from login.models import User, Request, Advisor, Reservation, Notifiaction
from chat.models import Chat_User, Chat

from datetime import timedelta


class RequestConsumer(WebsocketConsumer):
    def connect(self):

        global answer, group_title, advisor, user

        if self.scope['path'][4:8] == 'user':
            print('user connected')
            advisor = get_object_or_404(Advisor, id=self.scope['url_route']['kwargs']['advisor_id'])
            group_title = self.scope['user'].id + advisor.id
            user = self.scope['user']
            request_content = self.scope['url_route']['kwargs']['request_content']
            Request.objects.create(sender=user, receiver=advisor, request_content=request_content)
            print('request created')
            Notifiaction.objects.create(type='r', user_id=advisor.id)
            print('notification created')


        else:
            request_id = self.scope['url_route']['kwargs']['request_id']
            answer = self.scope['url_route']['kwargs']['answer']
            print('advisor connected')
            print(request_id)
            print(answer)
            request = get_object_or_404(Request, id=request_id, receiver=self.scope['user'])
            # user = request.sender
            request.is_checked = True
            request.is_accepted = True if (answer == 1) else False
            request.save()
            group_title = request.sender.id + self.scope['user'].id

        async_to_sync(self.channel_layer.group_add)(
            group_title,
            self.channel_name
        )
        self.accept()

        if answer == 1:
            self.accept_response(advisor, user)
        elif answer == 0:
            self.reject_response()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            group_title,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def reject_response(self):

        print('rejected')
        self.send(text_data=json.dumps({
            'message': 0,
            'chat': '',
            'reservation': ''
        }))

    def accept_response(self, advisor, user):

        print('accepted')
        chat_title = user.email + ' ' + advisor.email
        chat = Chat.objects.create(title=chat_title)
        Chat_User.objects.create(chat_start_datetime=chat.time_started,
                                 end_session_datetime=chat.time_started + timedelta(
                                     minutes=60),
                                 chat_id=chat.id,
                                 user_id=user.id)
        Chat_User.objects.create(chat_start_datetime=chat.time_started,
                                 end_session_datetime=chat.time_started + timedelta(
                                     minutes=60),
                                 chat_id=chat.id,
                                 user_id=advisor.id)
        reservation = Reservation.objects.create(user_id=user.id,
                                                 advisor_user_id=advisor,
                                                 reservation_datetime=chat.time_started,
                                                 end_session_datetime=chat.time_started + timedelta(
                                                     minutes=60))
        self.send(text_data=json.dumps({
            'message': 1,
            'chat': chat,
            'reservation': reservation
        }))