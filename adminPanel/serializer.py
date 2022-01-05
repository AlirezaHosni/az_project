from django.contrib.auth.hashers import make_password

import login
from chat import serializers
from login.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'gender', 'year_born',
                  'is_advisor', 'image']

    def update(self, instance, validated_data):
        password = validated_data.get('password')

        if password is not None:
            super(UserSerializer, self).update(instance, validated_data)
            instance.password = make_password(validated_data.get('password', instance.password))
            instance.save()
        else:
            super(UserSerializer, self).update(instance, validated_data)

        return instance