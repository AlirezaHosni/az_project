from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions

from login.serializer import CreateInvitationSerializer


class CreateUserByAdmin(generics.CreateAPIView):

    serializer_class = CreateInvitationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]



