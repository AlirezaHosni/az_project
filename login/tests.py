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



class RegisterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@a.co", password="2",
                                        phone_number="1234",
                                        first_name="mammad",
                                        last_name="mama", is_advisor=False,
                                        gender="M", year_born="2021-07-17 08:27:03",
                                        )
        self.token = Token.objects.create(user=self.user)
        print(self.token)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)



    def test_user_can_register(self):
       	# img = BytesIO(b'C:/Users/AmirHossein/Pictures/Screenshots/Screenshot (3).png')
        # img = open('C:/Users/AmirHossein/Pictures/Screenshots/Screenshot (3).png', encoding="utf8")
        # img = SimpleUploadedFile("C:/Users/AmirHossein/Pictures/Screenshots/Screenshot (3).png", b"file_content")

        file = io.BytesIO(b'C:/Users/AmirHossein/Pictures/Screenshots/Screenshot (3).png')
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        

        data = {
                "email":"rr@poi.co",
                "password":"2",
                "phone_number":"1094522",
                "first_name":"aa",
                "gender":"M",
                "year_born":"2021-07-17 08:27:03",
                "last_name":"bb",
                "is_advisor":True,
                "is_mental_advisor": True,
                "is_family_advisor": True,
                "is_sport_advisor": True,
                "is_healthcare_advisor": True,
                "is_ejucation_advisor": True,
                "meli_code": "4090084",
                "advise_method": "on",
                "address": "shkfjsdkj",
                "telephone": "64387958",
                "doc_images": [file]
            }
        response = self.client.post('/api/signup/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    

    def test_user_can_see_profile(self):
        response = self.client.get('/api/user-profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_can_logout(self):
        response = self.client.get('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)