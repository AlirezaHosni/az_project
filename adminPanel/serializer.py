from django.contrib.auth.hashers import make_password

import login
from rest_framework import serializers
from login.models import User, Advisor_History, Advisor, Rate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'gender', 'year_born','is_advisor', 'image']
        read_only_fields = ['id']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['advisor', 'user', 'text', 'rate', 'created_at', 'is_confirmed']


class ListUsersInfoSerializer(serializers.ModelSerializer):
    hour_of_session = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['id', 'email', 'num_of_session', 'hour_of_session', 'password', 'first_name', 'last_name', 'phone_number', 'gender', 'year_born','is_advisor', 'image']
