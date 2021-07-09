from re import T
from django.contrib.auth import authenticate
from django.db.models import fields
from django.http import request
from knox import models
from rest_framework import serializers
from rest_framework.exceptions import server_error
from rest_framework.fields import ReadOnlyField
from .models import Advisor, User, Request
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password','first_name','last_name','phone_number','gender','year_born','is_advisor','image']
       

    def update(self, instance, validated_data):
        super(UserSerializer, self).update(instance, validated_data)
        
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
        


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Advisor
        fields = '__all__'
        read_only_fields = ['user']









class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    year_born = serializers.DateTimeField()
    is_advisor = serializers.BooleanField()
    image = serializers.ImageField()


    is_mental_advisor = serializers.BooleanField(allow_null=True)
    is_family_advisor = serializers.BooleanField(allow_null=True)
    is_sport_advisor = serializers.BooleanField(allow_null=True)
    is_healthcare_advisor = serializers.BooleanField(allow_null=True)
    is_ejucation_advisor = serializers.BooleanField(allow_null=True)
    meli_code = serializers.CharField(allow_null=True)
    advise_method = serializers.CharField(allow_null=True)
    address = serializers.CharField(allow_null=True)
    telephone = serializers.CharField(allow_null=True)

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')

    #     if email and password:
    #         user = authenticate(request=self.context.get('request'),
    #             email=email, password=password)

    #         if user:
    #             raise
    #     else:
    #         raise

    #     return attrs

    def create(self, validated_data):
        
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'],
            phone_number=validated_data['phone_number'], first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],is_advisor=validated_data['is_advisor'],
            gender=validated_data['gender'], year_born=validated_data['year_born'], 
            image=validated_data['image'])    

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
                    telephone=validated_data['telephone'])   

        return user  


class SearchInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    year_born = serializers.DateTimeField()
    image = serializers.ImageField()


    is_mental_advisor = serializers.BooleanField(allow_null=True)
    is_family_advisor = serializers.BooleanField(allow_null=True)
    is_sport_advisor = serializers.BooleanField(allow_null=True)
    is_healthcare_advisor = serializers.BooleanField(allow_null=True)
    is_ejucation_advisor = serializers.BooleanField(allow_null=True)
    meli_code = serializers.CharField(allow_null=True)
    advise_method = serializers.CharField(allow_null=True)
    address = serializers.CharField(allow_null=True)
    telephone = serializers.CharField(allow_null=True)



class RequestSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    image = serializers.ImageField()

    #request model fields
    id = serializers.CharField()
    request_content = serializers.CharField()
    is_checked = serializers.BooleanField()
    is_blocked = serializers.BooleanField()
    is_accepted = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    is_Done = serializers.BooleanField()


class RequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['is_checked','is_accepted', 'is_blocked']

    # def update(self, instance, validated_data):
    #     super(RequestUpdateSerializer, self).update(instance, validated_data)
        
    #     instance.is_accepted = validated_data.get('is_accepted', instance.is_accepted)
    #     instance.is_blocked = validated_data.get('is_blocked', instance.is_blocked)
    #     instance.save()
    #     return instance


class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['request_content', 'receiver']

    def create(self, validated_data):
        return Request.objects.create(request_content=validated_data['request_content'],
            receiver_id=validated_data['receiver'].id, sender_id=self.context['request'].user.id)



# class RateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ...
#         fields = []

#     def create(self, validated_data):
#         return ....objects.create(validated_data())
