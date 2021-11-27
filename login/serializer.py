from re import T
from django.contrib.auth import authenticate
from django.db.models import fields
from django.http import request
from knox import models
from rest_framework import serializers
from rest_framework.exceptions import server_error
from rest_framework.generics import get_object_or_404
from .models import Advisor, User, Request, Rate, Advisor_History, Advisor_Document , Invitation, Notifiaction
from django.contrib.auth.hashers import make_password


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


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):

        if validated_data['meli_code'] is not None:
            isDuplicate_code = Advisor.objects.filter(meli_code=validated_data['meli_code'])
            if isDuplicate_code.count() >= 1:
                raise serializers.ValidationError('meli_code')

        return Advisor.objects.create(user_id=self.context['request'].user.id,
                                      is_mental_advisor=validated_data['is_mental_advisor'],
                                      is_family_advisor=validated_data['is_family_advisor'],
                                      is_sport_advisor=validated_data['is_sport_advisor'],
                                      is_healthcare_advisor=validated_data['is_healthcare_advisor'],
                                      is_ejucation_advisor=validated_data['is_ejucation_advisor'],
                                      meli_code=validated_data['meli_code'],
                                      advise_method=validated_data['advise_method'],
                                      address=validated_data['address'],
                                      telephone=validated_data['telephone'])


class RegisterSerializer(serializers.Serializer):
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
    doc_images = serializers.ListField(child=serializers.ImageField(), allow_empty=True)


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
                                             
            for image in validated_data['doc_images']:
                Advisor_Document.objects.create(advisor_id=advisor.id,
                                                doc_image=image
                                                )

        return user


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


class SearchInfoSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    id = serializers.CharField()
    rate = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    number_of_rates = serializers.IntegerField()
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
    sender_id = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    image = serializers.ImageField()

    # request model fields
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
                                      receiver_id=validated_data['receiver'].id,
                                      sender_id=self.context['request'].user.id)


class CreateInvitationSerializer(serializers.ModelSerializer):

    student_id = serializers.IntegerField(write_only=True)
    advisor = UserSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ['invitation_content', 'advisor', 'student', 'student_id']

    def create(self, validated_data):
        
        student = get_object_or_404(User,id=validated_data.pop('student_id'))
        advisor_user = get_object_or_404(User,email=self.context['request'].user.email)
        advisor = get_object_or_404(Advisor,User=advisor_user)

        validated_data['advisor'] = advisor
        validated_data['student'] = student

        Notifiaction.objects.create(user=student, type='i', contacts=advisor)

        instance = super().create(validated_data)

        return instance


class ListInvitationSerializer(serializers.ModelSerializer):

    advisor = AdvisorSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ['advisor','student','invitation_content','created_at']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['text', 'rate', 'advisor']

    def create(self, validated_data):
        return Rate.objects.create(text=validated_data['text'],
                                   rate=validated_data['rate'], user_id=self.context['request'].user.id,
                                   advisor_id=validated_data['advisor'].id)


class ListRateSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    text = serializers.CharField()
    rate = serializers.CharField()
    created_at = serializers.DateTimeField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.ImageField()


class AdvisorResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor_History
        fields = ['id', 'granted_prize']

    def create(self, validated_data):
        return Advisor_History.objects.create(advisor_id=Advisor.objects.get(user=self.context['request'].user.id).id,
                                              granted_prize=validated_data['granted_prize'])


class RequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['is_checked', 'is_accepted', 'is_blocked', 'sender']
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


class AdvisorDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor_Document
        fields = '__all__'

        def create(self, validated_data):
            return Advisor_Document.objects.create(advisor_id=Advisor.objects.get(user=self.context['request'].user.id).id,
                                                doc_image=validated_data['doc_image'])



class ListNotifiactionSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    contacts = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Notifiaction
        fields = fields = ['user', 'type', 'contacts', 'created_at']
