from re import T
from django.contrib.auth import authenticate
from django.db.models import fields
from django.http import request
from knox import models
from rest_framework import serializers
from rest_framework.exceptions import server_error
from .models import Advisor, User, Request, Rate, Advisor_History
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

    def create(self, validated_data):
        return Advisor.objects.create(user_id=self.context['request'].user.id, 
            is_mental_advisor = validated_data['is_mental_advisor'],
            is_family_advisor = validated_data['is_family_advisor'],
            is_sport_advisor = validated_data['is_sport_advisor'],
            is_healthcare_advisor = validated_data['is_healthcare_advisor'],
            is_ejucation_advisor = validated_data['is_ejucation_advisor'],
            meli_code = validated_data['meli_code'],
            advise_method = validated_data['advise_method'],
            address= validated_data['address'],
            telephone = validated_data['telephone'])


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    year_born = serializers.DateTimeField()
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
           )

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
    id = serializers.CharField()
    rate = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
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

 

class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['request_content', 'receiver']

    def create(self, validated_data):
        return Request.objects.create(request_content=validated_data['request_content'],
            receiver_id=validated_data['receiver'].id, sender_id=self.context['request'].user.id)



class RateSerializer(serializers.ModelSerializer):
     class Meta:
         model = Rate
         fields = ['text', 'rate', 'advisor']

     def create(self, validated_data):
         return Rate.objects.create(text=validated_data['text'],
          rate=validated_data['rate'], user_id=self.context['request'].user.id, 
          advisor_id=validated_data['advisor'].id)



class ListRateSerializer(serializers.Serializer):
    text = serializers.CharField()
    rate = serializers.CharField()
    created_at = serializers.DateTimeField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.ImageField()
    

class AdvisorResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor_History
        fields = ['id','granted_prize']

    def create(self, validated_data):
         return Advisor_History.objects.create(advisor_id=Advisor.objects.get(user=self.context['request'].user.id).id,
         granted_prize=validated_data['granted_prize'])


class RequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ['is_checked','is_accepted', 'is_blocked', 'sender']
        read_only_fields = ['sender']
        

class professionFinder(serializers.Serializer):
    profession = serializers.CharField()
   

class RateFinderSerializer(serializers.Serializer):
    advisor_id = serializers.CharField()


class AdvisorInfoSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
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

    rate = serializers.CharField()
    advisor_id = serializers.CharField()
    
