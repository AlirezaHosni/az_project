from django.db import models
from login.models import User

# Create your models here.
class Chat(models.Model):
    time_started = models.DateTimeField(auto_now_add=True)
    time_changed = models.DateTimeField(null=True,blank=True)
    title = models.CharField(max_length=255,unique=True,error_messages={
            'unique': "هر چت فقط یکبار میتواند ساخته شود",
        })

    def __str__(self):
        ''' String presenting an ChatBox object '''
        return self.title

    class Meta:
        ordering = ['-time_changed']


class Chat_User(models.Model):

    chat = models.ForeignKey("Chat",on_delete=models.CASCADE,related_name='chats_users')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='users_chat')
    is_done = models.BooleanField(default=False)
    chat_start_datetime = models.DateTimeField()
    end_session_datetime = models.DateTimeField()


class Message(models.Model):

    chat = models.ForeignKey("Chat",on_delete=models.CASCADE,related_name='chats_message')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_message')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_short_text()

    class Meta:
        ordering = ['-date']

    def get_short_text(self):
        limit = 50
        return self.text[:limit] + ('...' if len(self.text) > limit else '')

    get_short_text.short_description = 'متن پیام'
