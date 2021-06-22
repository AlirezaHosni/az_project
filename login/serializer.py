from re import T
from django.contrib.auth import authenticate
from django.db.models import fields
from rest_framework import serializers
from rest_framework.exceptions import server_error
from rest_framework.fields import ReadOnlyField
from .models import Advisor, User
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





# Register Serializer
# class RegisterUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','email', 'password', 'phone_number', 'first_name', 'last_name', 
#             'gender', 'year_born', 'is_advisor']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'],phone_number=validated_data['phone_number'], first_name=validated_data['first_name'], last_name=validated_data['last_name'],is_advisor=validated_data['is_advisor'])            
#         return user





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

    is_religious_advisor = serializers.BooleanField(allow_null=True)

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
                    is_religious_advisor=validated_data['is_religious_advisor'],
                    is_healthcare_advisor=validated_data['is_healthcare_advisor'],
                    is_ejucation_advisor=validated_data['is_ejucation_advisor'],
                    meli_code=validated_data['meli_code'],
                    advise_method=validated_data['advise_method'],
                    address=validated_data['address'],
                    telephone=validated_data['telephone'])   

        return user  


class SearchSerializer(serializers.Serializer):

    fullname = serializers.CharField(allow_blank=True)

class SearchInfoSerializer(serializers.Serializer):
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

    is_religious_advisor = serializers.BooleanField(allow_null=True)

    is_healthcare_advisor = serializers.BooleanField(allow_null=True)

    is_ejucation_advisor = serializers.BooleanField(allow_null=True)

    meli_code = serializers.CharField(allow_null=True)

    advise_method = serializers.CharField(allow_null=True)

    address = serializers.CharField(allow_null=True)

    telephone = serializers.CharField(allow_null=True)
