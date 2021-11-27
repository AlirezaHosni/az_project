# import unittest
from login.models import User, Advisor, Advisor_Document, Advisor_History
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
        self.user = User.objects.create_user(
            email="a@a.co", password="2",
            phone_number="1234",
            first_name="mammad",
            last_name="mama", is_advisor=False,
            gender="M", year_born="2021-07-17 08:27:03",
        )
        self.user2 = User.objects.create_user(
            email="b@b.co", password="2",
            phone_number="1234445",
            first_name="ali",
            last_name="baba", is_advisor=True,
            gender="M", year_born="2021-07-17 08:27:03",
        )
        self.advisor = Advisor.objects.create(
            is_mental_advisor= True,
            is_family_advisor= False,
            is_sport_advisor= False,
            is_healthcare_advisor= False,
            is_ejucation_advisor= False,
            meli_code= "5824090084",
            advise_method= "on",
            address= "shkfjsdkj",
            telephone= "55387958",
            user_id = self.user2.id
        )
        self.advisor_doc = Advisor_Document.objects.create(
            doc_image = "Documents/Screenshot_283_HC31hdt.png",
            advisor_id = self.advisor.id
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


    def test_user_can_send_request(self):
        data = {
            "request_content": "hi how you doing",
            "receiver": self.advisor.id
        }
        res = self.client.post('/api/send-request/', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    
    def test_user_can_register_as_advisor(self):
        data1 = {
            "is_mental_advisor": True,
            "is_family_advisor": True,
            "is_sport_advisor": True,
            "is_healthcare_advisor": True,
            "is_ejucation_advisor": True,
            "meli_code": "23423",
            "advise_method": "on",
            "address": "string",
            "telephone": "242443"
        }
        data2 = {
            "is_advisor": True
        }

        advisor_created_response = self.client.post('/api/create-advisor/', data1)
        self.assertEqual(advisor_created_response.status_code, status.HTTP_201_CREATED)

        user_as_advisor_response = self.client.patch('/api/user-profile/', data2)
        self.assertEqual(user_as_advisor_response.status_code, status.HTTP_200_OK)

    def test_user_can_logout(self):
        response = self.client.get('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_user_can_search_advisors(self):
    #     response = self.client.get('/api/search/' + 'baba/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdvisorStuffTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="b@b.co", password="2",
            phone_number="1234445",
            first_name="ali",
            last_name="baba", is_advisor=True,
            gender="M", year_born="2021-07-17 08:27:03",
        )
        self.advisor = Advisor.objects.create(
            is_mental_advisor= True,
            is_family_advisor= False,
            is_sport_advisor= False,
            is_healthcare_advisor= False,
            is_ejucation_advisor= False,
            meli_code= "5824090084",
            advise_method= "on",
            address= "shkfjsdkj",
            telephone= "55387958",
            user_id = self.user.id
        )
        self.advisor_doc = Advisor_Document.objects.create(
            doc_image = "Documents/Screenshot_283_HC31hdt.png",
            advisor_id = self.advisor.id
        )
        self.advisor_resume = Advisor_History.objects.create(
            advisor_id= self.advisor.id,
            granted_prize= "something from some place"
        )
        self.user2 = User.objects.create_user(
            email="a@a.co", password="2",
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


    # def test_advisor_can_send_invitation(self):
    #     data = {
    #         "invitation_content": "do you wanna chat about yourself?",
    #         "student_id": self.user2.id
    #     }
    #     res = self.client.post('/api/send-invitation/', data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_advisor_can_make_resume(self):
        data = {
            "granted_prize": "blah blah blah"
        }
        response = self.client.post('/api/advisor-resume/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_advisor_can_list_resume(self):
        response = self.client.get('/api/advisor-resume/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_advisor_can_update_resume(self):
        data = {
            "granted_prize": "  blah"
        }
        response = self.client.put('/api/update-advisor-resume/'+ str(self.advisor_resume.id) +'/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_profile_image(self):
        response = self.client.get('/api/get-profile-image/'+ str(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

##
    def test_user_can_get_profile_info(self):
        response = self.client.get('/api/user-profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_cannot_get_another_user_profile(self):
    #     response = self.client.get('/api/advisor-resume/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_can_update_profile(self):
        data = {
            "firstname": "blah blah",
            "password": "12345678"
        }
        response = self.client.put('/api/user-profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_test_user_cannot_update_another_user_profile(self):
    #     data = {
    #         "granted_prize": "blah blah blah"
    #     }
    #     response = self.client.put('/api/update-advisor-resume/'+ str(self.advisor_resume.id) +'/', data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    


    
