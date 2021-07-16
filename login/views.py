import datetime
from re import search
from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_object_or_404, render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from yaml.tokens import FlowEntryToken
from .models import Advisor, User, Request, Rate, Advisor_History
from .serializer import RateFinderSerializer, AdvisorInfoSerializer, professionFinder, AdvisorResumeSerializer, ListRateSerializer, RateSerializer, CreateRequestSerializer, RequestUpdateSerializer, RequestSerializer, SearchInfoSerializer,RegisterSerializer,UserSerializer,AdvisorSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import mixins, permissions
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework import filters
from django.http import HttpResponse
from .custom_renderer import JpegRenderer, PngRenderer
#run this command for knox
#   pip install django-rest-knox
#   pip install drf-spectacular



class SignUpAPI(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        # "user": UserSerializer(user).data,
        "token": AuthToken.objects.create(user)[1]
        })



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserInfoAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super(UserInfoAPI, self).update(request, *args, **kwargs)


class AdvisorInfoAPI(generics.RetrieveUpdateAPIView):
    serializer_class = AdvisorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return Advisor.objects.get(user_id=self.request.user.id)


class SearchAdvisorAPI(generics.ListAPIView):
    serializer_class = SearchInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)
   

    def get_queryset(self):
        search_name = self.request.GET.get('search')
        return User.objects.raw('select res.id,COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_rate as r right join (select a.id,first_name,last_name,year_born,email,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id where first_name like %s or last_name like %s) as res on advisor_id =res.id group by res.id order by rate desc', ["%"+search_name+"%", "%"+search_name+"%"])
    

class SendRequestAPI(generics.CreateAPIView):
    serializer_class = CreateRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    


class RequestsInfoAPI(generics.ListAPIView):
    serializer_class= RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def get_queryset(self):
        return Request.objects.raw('select email,first_name,last_name,gender,image,r.id,request_content,is_checked,is_blocked,is_accepted,created_at,is_Done from login_user as u inner join login_request as r on u.id = r.sender_id where u.id = %s', [self.request.user.id])


class AdvisorRequestsInfoAPI(generics.ListAPIView):
    serializer_class= RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def get_queryset(self):
        return Request.objects.raw('select email,first_name,last_name,gender,image,r.id,request_content,is_checked,is_blocked,is_accepted,created_at,is_Done from login_user as u inner join login_request as r on u.id=r.sender_id where r.receiver_id in (select a.id from login_advisor as a inner join login_user as u on a.user_id=u.id where u.id=%s) and is_checked=false', [self.request.user.id])


class RequestUpdateStatus(generics.UpdateAPIView):
    serializer_class = RequestUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
   
    def get_object(self):
        return Request.objects.get(id = self.kwargs['id'])



class CreateRateAPI(generics.CreateAPIView):
    serializer_class=RateSerializer
    permission_classes = (permissions.IsAuthenticated,)



    

class ListRateAPI(generics.ListAPIView):
    serializer_class= ListRateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
         return Rate.objects.raw('select rate.id, rate.text, rate.rate, rate.created_at , user.first_name, user.last_name, user.image  from login_rate as rate inner join login_user as user on rate.user_id=user.id where rate.advisor_id in (select a.id from login_advisor as a inner join login_user as u on a.user_id=u.id where u.id=%s)', [self.request.user.id])


class ListRateByAdvisorIdAPI(generics.ListAPIView):
    serializer_class= ListRateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        serialized = RateFinderSerializer(data=self.request.data)
        serialized.is_valid()
        advisor_id = serialized.validated_data['advisor_id']
        return Rate.objects.raw('select rate.id, rate.text, rate.rate, rate.created_at , user.first_name, user.last_name, user.image  from login_rate as rate inner join login_user as user on rate.user_id=user.id where rate.advisor_id in (select a.id from login_advisor as a inner join login_user as u on a.user_id=u.id where a.id=%s)', [advisor_id])


class ListAdvisorResumeAPI(generics.ListCreateAPIView):
    serializer_class = AdvisorResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        advisor = Advisor.objects.get(user=self.request.user.id)
        return Advisor_History.objects.raw('select id, granted_prize from login_advisor_history where advisor_id=%s', [advisor.id])


class UpdateAdvisorResumeAPI(generics.UpdateAPIView):
    serializer_class = AdvisorResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return Advisor_History.objects.get(id=self.kwargs['granted_prize_id'])

#destroy


class CreateAdvisor(generics.CreateAPIView):
    serializer_class = AdvisorSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GetAllAdvisorsAPI(generics.ListAPIView):
    serializer_class = SearchInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.raw('select res.id,COUNT(rate) as number_of_rates,avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_rate as r right join (select a.id,first_name,last_name,year_born,email,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id) as res on advisor_id =res.id group by res.id order by rate desc') 


# class GetParticularAdvisorsAPI(generics.ListAPIView):
#     serializer_class = SearchInfoSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         serilized = professionFinder(data=self.request.data)
#         serilized.is_valid()
#         profession = serilized.validated_data['profession']
#         value = serilized.validated_data['value']
#         return User.objects.raw('select * from login_user as u inner join login_advisor as a on u.id = a.user_id where '+profession+' = %s', [value]) 


# class GetParticularAdvisorCommentsAPI(generics.ListAPIView):

class BestAdvisorsByProfessionAPI(generics.ListAPIView):
    serializer_class=SearchInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        serilized = professionFinder(data=self.request.data)
        serilized.is_valid()
        profession = serilized.validated_data['profession']
        
        return Advisor.objects.raw('select r.id,advisor_id,COUNT(rate),avg(rate) as rate,first_name,last_name,email,year_born,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_rate as r inner join (select a.id,first_name,last_name,year_born,email,phone_number,gender,image,is_mental_advisor,is_family_advisor,is_sport_advisor, is_healthcare_advisor,is_ejucation_advisor,meli_code,advise_method,address,telephone from login_user as u inner join login_advisor as a on u.id = a.user_id where '+profession+' = true) as res on advisor_id =res.id group by advisor_id order by rate desc')

    
    
  
class GetUserImageAPI(APIView):
    
    def get(self, request):
        img = User.objects.get(id = self.request.user.id).image
        return HttpResponse(img, content_type="image/png")

    
    
class ImageApiView(generics.RetrieveAPIView):

    renderer_classes = [JpegRenderer]

    def get(self, request, *args, **kwargs):
        queryset = User.objects.get(id=self.kwargs['id']).image
        data = queryset
        return Response(data, content_type='image/jpg')
