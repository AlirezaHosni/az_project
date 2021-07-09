from re import search
from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import get_object_or_404, render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import Advisor, User, Request
from .serializer import RequestUpdateSerializer, RequestSerializer, SearchInfoSerializer,RegisterSerializer,UserSerializer,AdvisorSerializer
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
        return User.objects.raw('select * from login_user as u inner join login_advisor as a on u.id = a.user_id where first_name like %s or last_name like %s', ["%"+search_name+"%", "%"+search_name+"%"])
    
    

class RequestsInfoAPI(generics.ListAPIView):
    serializer_class= RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def get_queryset(self):
        return Request.objects.raw('select email,first_name,last_name,gender,image,r.id,request_content,is_checked,is_blocked,is_accepted,created_at,is_Done from login_user as u inner join login_request as r on u.id = r.sender_id where u.id = %s', [self.request.user.id])


class AdvisorRequestsInfoAPI(generics.ListAPIView):
    serializer_class= RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def get_queryset(self):
        return Request.objects.raw('select email,first_name,last_name,gender,image,r.id,request_content,is_checked,is_blocked,is_accepted,created_at,is_Done from login_user as u inner join login_request as r on u.id=r.sender_id where r.receiver_id in (select a.id from login_advisor as a inner join login_user as u on a.user_id=u.id where u.id=%s)', [self.request.user.id])


class RequestUpdateStatus(generics.UpdateAPIView):
    serializer_class = RequestUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
   

    # def update(self, request, *args, **kwargs):
    #     return super(RequestUpdateStatus, self).update(request, *args, **kwargs)

    def get_object(self, pk):
        return Request.objects.get(id = pk)

    # def get_queryset(self):
    #     return Request.objects.raw('update login_request set is_checked = true, is_accepted=%s, is_blocked=%s where id=%s', [self.request.POST.get('is_accepted'), self.request.POST.get('is_blocked'), self.request.POST.get('id')])
   

   
