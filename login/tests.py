# import unittest
from login.models import User
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from io import BytesIO
# from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
import base64

# Create your tests here.

