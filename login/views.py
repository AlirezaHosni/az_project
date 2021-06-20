from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import Advisor, User
from .serializer import RegisterSerializer,UserSerializer,AdvisorSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics


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


class AdvisorInfoAPI(generics.RetrieveUpdateAPIView):
    serializer_class = AdvisorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return Advisor.objects.get(user_id=self.request.user.id)

