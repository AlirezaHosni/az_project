from django.contrib.auth.hashers import make_password

import login
from rest_framework import serializers
from login.models import User, Advisor_History, Advisor, Rate, Reservation
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'gender', 'year_born','is_advisor']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'],
                                        phone_number=validated_data['phone_number'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'], is_advisor=False,
                                        gender=validated_data['gender'], year_born=validated_data['year_born'],
                                        email_confirmed_at=datetime.datetime.now())
        return user
        


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['advisor', 'user', 'text', 'rate', 'created_at', 'is_confirmed']


class ListUsersInfoSerializer(serializers.ModelSerializer):
    hour_of_session = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['id', 'email', 'num_of_session', 'hour_of_session', 'password', 'first_name', 'last_name', 'phone_number', 'gender', 'year_born','is_advisor', 'image']


class createAdvisorSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    year_born = serializers.DateTimeField(allow_null=True)
    is_advisor = serializers.BooleanField()

    is_mental_advisor = serializers.BooleanField(allow_null=True)
    is_family_advisor = serializers.BooleanField(allow_null=True)
    is_sport_advisor = serializers.BooleanField(allow_null=True)
    is_healthcare_advisor = serializers.BooleanField(allow_null=True)
    is_ejucation_advisor = serializers.BooleanField(allow_null=True)
    meli_code = serializers.CharField(allow_null=True)
    advise_method = serializers.CharField(allow_null=True)
    address = serializers.CharField(allow_null=True)
    telephone = serializers.CharField(allow_null=True)

    def create(self, validated_data):

        duplicates = ''

        isDuplicate_email = User.objects.filter(email=validated_data['email'])
        if isDuplicate_email.count() >= 1:
            duplicates = duplicates + 'email and '

        isDuplicate_phone = User.objects.filter(phone_number=validated_data['phone_number'])
        if isDuplicate_phone.count() >= 1:
            duplicates = duplicates + 'phon and '

        if validated_data['meli_code'] is not None:
            isDuplicate_code = Advisor.objects.filter(meli_code=validated_data['meli_code'])
            if isDuplicate_code.count() >= 1:
                duplicates = duplicates + 'meli code and '

        if duplicates != '':
            duplicates = duplicates[:len(duplicates) - 5]
            raise serializers.ValidationError(duplicates)

        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'],
                                        phone_number=validated_data['phone_number'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'], is_advisor=validated_data['is_advisor'],
                                        gender=validated_data['gender'], year_born=validated_data['year_born'],
                                        email_confirmed_at=datetime.datetime.now()
                                        )

        # email_verification_token = Email_Verification.objects.create(
        #     user_id=user.id,
        #     key=secrets.token_urlsafe(8)
        # )

        if user.is_advisor == True:
            advisor = Advisor.objects.create(user_id=user.id,
                                             is_mental_advisor=validated_data['is_mental_advisor'],
                                             is_family_advisor=validated_data['is_family_advisor'],
                                             is_sport_advisor=validated_data['is_sport_advisor'],
                                             is_healthcare_advisor=validated_data['is_healthcare_advisor'],
                                             is_ejucation_advisor=validated_data['is_ejucation_advisor'],
                                             meli_code=validated_data['meli_code'],
                                             advise_method=validated_data['advise_method'],
                                             address=validated_data['address'],
                                             telephone=validated_data['telephone'],
                                             is_verified=True)

            
        return user


class getAdvisorListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    # session_numbers = serializers.IntegerField()#
    average_rate = serializers.IntegerField()
    created_on = serializers.DateTimeField()
    # daily_begin_time = serializers.DateTimeField()#
    # daily_end_time = serializers.DateTimeField()#


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rate
        fields='__all__'
        read_only_fields=['id','advisor_id','user_id']
    

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'
        read_only_fields=['id','advisor_user_id','user_id']



class AdvisorSerializer(serializers.ModelSerializer):
    first_name= serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    year_born = serializers.DateTimeField()
    class Meta:
        model = Advisor
        fields = '__all__'
        read_only_fields = ['user_id']