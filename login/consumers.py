import random
import string

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import channels.layers

from rest_framework.generics import get_object_or_404
from login.models import User, Request, Advisor, Reservation, Notifiaction
from chat.models import Chat_User, Chat
from rest_framework.authtoken.models import Token

from datetime import timedelta


class RequestConsumer(WebsocketConsumer):
    def connect(self):

        self.answer = False
        self.group_title = ''.join((random.choice(string.ascii_lowercase) for x in range(30)))

        if self.scope['path'][4:8] == 'user':

            try:
                token = self.scope['url_route']['kwargs']['token']
                # print(token)
                self.user_id = Token.objects.get(key=token).user_id
                # print(self.user_id)
                self.user = get_object_or_404(User, id=self.user_id)
                # print('user connected')
                self.advisor = get_object_or_404(Advisor, id=self.scope['url_route']['kwargs']['advisor_id'])
                self.group_title = self.user.id + self.advisor.id
                request_content = self.scope['url_route']['kwargs']['request_content']
                Request.objects.create(sender=self.user, receiver=self.advisor, request_content=request_content)
                # print('request created')
                # Notifiaction.objects.create(type='r', user_id=self.advisor.id)
                # print('notification created')
                self.accept()
            except(Token.DoesNotExist):
                return {
                    "error": "این کاربر ناشناخته هست. ابتدا  وارد سایت شوید"
                }


        else:

            try:
                token = self.scope['url_route']['kwargs']['token']
                self.adviser_id = Token.objects.get(key=token).user_id
                self.advisor = get_object_or_404(Advisor, user_id=self.adviser_id)
                request_id = self.scope['url_route']['kwargs']['request_id']
                self.answer = self.scope['url_route']['kwargs']['answer']
                request = get_object_or_404(Request, id=request_id, receiver=self.advisor)
                self.user = request.sender
                request.is_checked = True
                request.is_accepted = True if (self.answer == 1) else False
                request.save()
                self.group_title = self.user.id + self.advisor.id

                self.accept()

                if self.answer == 1:
                    self.accept_response(self.advisor, self.user)
                elif self.answer == 0:
                    self.reject_response()


            except(Token.DoesNotExist):
                return {
                    "error": "این کاربر ناشناخته هست. ابتدا  وارد سایت شوید"
                }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_title,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def reject_response(self):


        self.send(text_data=json.dumps({
            'answer': 'rejected',
            'chat_id': '',
            'reservation_id': ''
        }))

    def accept_response(self, advisor, user):


        chat_title = user.email + ' ' + advisor.user.email
        is_duplicate_chat = Chat.objects.filter(title=chat_title)
        if is_duplicate_chat.count == 0:
            chat = Chat.objects.create(title=chat_title)
        else:
            chat = is_duplicate_chat.first()
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
                                                 advisor_user_id=advisor.id,
                                                 reservation_datetime=chat.time_started,
                                                 end_session_datetime=chat.time_started + timedelta(
                                                     minutes=60))
        self.send(text_data=json.dumps({
            'answer': 'accepted',
            'chat_id': chat.id,
            'reservation_id': reservation.id,
            # 'reservation_datetime': reservation.reservation_datetime,
            # 'end_session_datetime': reservation.end_session_datetime
        }))
