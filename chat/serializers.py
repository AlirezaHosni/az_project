from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from login.models import User
from .models import Chat,Chat_User,Message
from login.serializer import UserSerializer


class CreateChatSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    advisor = UserSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['student_id', 'advisor', 'title','student','time_changed','id']
        read_only_fields = ['advisor', 'title','student','time_changed','id']

    def create(self, validated_data):

        student = get_object_or_404(User,id=validated_data.pop('student_id'))
        advisor = get_object_or_404(User,email=self.context['request'].user.email)

        if student.id == advisor.id:
            msg = 'یک فرد یه تنهایی نمیتواند یک چت را ایچاد کند'
            raise serializers.ValidationError(msg)

        isDuplicate = Chat.objects.filter(title=student.email + ' ' + advisor.email)
        if isDuplicate.count() >= 1:
            msg = 'هر چت فقط یکبار میتواند ساخته شود'
            raise serializers.ValidationError(msg)

        validated_data['title'] = student.email + ' ' + advisor.email

        instance = super().create(validated_data)
        instance.time_changed = instance.time_started
        instance.save()
        Chat_User.objects.create(user=student, chat=instance)
        Chat_User.objects.create(user=advisor, chat=instance)

        validated_data['advisor'] = advisor
        validated_data['student'] = student
        validated_data['time_changed'] = instance.time_started
        validated_data['chat_id'] = instance.id

        return validated_data


class ChatListSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    chat = CreateChatSerializer(read_only=True)

    class Meta:
        model = Chat_User
        fields = ['chat','user']


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    chat = CreateChatSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['user', 'chat', 'text']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        chat = get_object_or_404(Chat,id=self.context.get('view').kwargs.get('id'))
        validated_data['chat'] = chat
        instance = super().create(validated_data)

        chat.time_changed = instance.date
        chat.save()

        return instance


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat_User
        fields = '__all__'