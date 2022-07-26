# import unittest
import datetime
from random import randint
from login.models import User, Advisor, Advisor_Document, Advisor_History, AdvisorDailyTime
from chat.models import Chat, Chat_User, Message
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
from django.utils import timezone
from datetime import timedelta


# Create your tests here.


class RegisterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="a@a.co", password="2",
            phone_number="1234",
            first_name="mammad",
            last_name="mama", is_advisor=False,
            gender="M", year_born=timezone.now(),
            is_active=True,
        )
        self.user2 = User.objects.create_user(
            email="b@b.co", password="2",
            phone_number="1234445",
            first_name="ali",
            last_name="baba", is_advisor=True,
            gender="M", year_born=timezone.now(),
            is_active=True,
        )
        self.advisor = Advisor.objects.create(
            is_mental_advisor=True,
            is_family_advisor=False,
            is_sport_advisor=False,
            is_healthcare_advisor=False,
            is_ejucation_advisor=False,
            meli_code="5824090084",
            advise_method="on",
            address="shkfjsdkj",
            telephone="55387958",
            user_id=self.user2.id
        )
        self.advisorDailyTime = AdvisorDailyTime.objects.create(
            job_time=[{
                "date": str(datetime.date.today()),
                "begin_time": str(datetime.datetime.now().time().strftime("%H:%M:%S")),
                "end_time": str((datetime.datetime.now() + datetime.timedelta(hours=8)).time().strftime("%H:%M:%S"))
            }],
            advisor_id=self.advisor.id
        )
        self.advisor_doc = Advisor_Document.objects.create(
            doc_file="Documents/Screenshot_283_HC31hdt.png",
            advisor_id=self.advisor.id
        )
        self.chat_intime = Chat.objects.create(
            time_started=timezone.now(),
            time_changed=timezone.now(),
            title="blah blah1"
        )
        self.chat_beforetime = Chat.objects.create(
            time_started=timezone.now(),
            time_changed=timezone.now(),
            title="blah blah2"
        )
        self.chat_aftertime = Chat.objects.create(
            time_started=timezone.now(),
            time_changed=timezone.now(),
            title="blah blah3"
        )
        self.chatuser = Chat_User.objects.create(
            chat=self.chat_intime,
            user=self.user,
            chat_start_datetime=timezone.now(),
            end_session_datetime=timezone.now() + timedelta(minutes=30)
        )
        self.chatuserDone = Chat_User.objects.create(
            chat=self.chat_aftertime,
            user=self.user,
            is_done=True,
            chat_start_datetime=timezone.now(),
            end_session_datetime=timezone.now() + timedelta(minutes=30)
        )
        self.chatuserNotStarted = Chat_User.objects.create(
            chat=self.chat_beforetime,
            user=self.user,
            chat_start_datetime=timezone.now() + timedelta(days=1),
            end_session_datetime=timezone.now() + timedelta(minutes=30)
        )
        self.chatuser2 = Chat_User.objects.create(
            chat=self.chat_intime,
            user=self.user2,
            chat_start_datetime=timezone.now(),
            end_session_datetime=timezone.now() + timedelta(minutes=30)
        )
        self.chatuserDone2 = Chat_User.objects.create(
            chat=self.chat_aftertime,
            user=self.user2,
            is_done=True,
            chat_start_datetime=timezone.now(),
            end_session_datetime=timezone.now() + timedelta(minutes=30)
        )
        self.chatuserNotStarted2 = Chat_User.objects.create(
            chat=self.chat_beforetime,
            user=self.user2,
            chat_start_datetime=timezone.now() + timedelta(days=1),
            end_session_datetime=timezone.now() + timedelta(minutes=30)
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

        # file = io.BytesIO(b'C:/Users/AmirHossein/Pictures/Screenshots/Screenshot (3).png')
        # image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        # image.save(file, 'png')
        # file.name = 'test.png'
        # file.seek(0)

        data = {
            "email": "a.h@gmail.com",
            "password": "2",
            "phone_number": "1094522",
            "first_name": "aa",
            "gender": "M",
            "year_born": "2021-07-17 08:27:03",
            "last_name": "bb",
            "is_advisor": True,
            "is_mental_advisor": True,
            "is_family_advisor": True,
            "is_sport_advisor": True,
            "is_healthcare_advisor": True,
            "is_ejucation_advisor": True,
            "meli_code": "4090084",
            "advise_method": "on",
            "address": "shkfjsdkj",
            "telephone": "64387958"
            # "doc_images": [file]
        }
        response = self.client.post('/api/signup/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_see_profile(self):
        response = self.client.get('/api/user-profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_can_send_request(self):
    #     data = {
    #         "request_content": "hi how you doing",
    #         "receiver": self.advisor.id
    #     }
    #     res = self.client.post('/api/send-request/', data)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

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
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_send_message_intime(self):
        response = self.client.post('/chat/send-message/' + str(self.chat_intime.id) + '/', {"text": "blah blah"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_send_message_beforetime(self):
        response = self.client.post('/chat/send-message/' + str(self.chat_beforetime.id) + '/', {"text": "blah blah"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_send_message_aftertime(self):
        response = self.client.post('/chat/send-message/' + str(self.chat_aftertime.id) + '/', {"text": "blah blah"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_reserve_session(self):
        reservation_data = {
            "receiver": self.user2.id,
            "reservation_datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration_min": randint(10, 60)
        }
        res = self.client.post('/api/list-or-create-reservation/', reservation_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # def test_user_cannot_comment_before_has_completed_chat(self):
    #     data = {
    #         "text":"blah",
    #         "rate":"3",
    #         "advisor":"1"
    #     }
    #     response = self.client.post('/api/create-comment/', data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test sending message from user2

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
            gender="M", year_born=timezone.now(),
            is_active=True,
        )
        self.advisor = Advisor.objects.create(
            is_mental_advisor=True,
            is_family_advisor=False,
            is_sport_advisor=False,
            is_healthcare_advisor=False,
            is_ejucation_advisor=False,
            meli_code="5824090084",
            advise_method="on",
            address="shkfjsdkj",
            telephone="55387958",
            user_id=self.user.id
        )
        self.advisor_doc = Advisor_Document.objects.create(
            doc_file="Documents/download-test.png",
            advisor_id=self.advisor.id
        )
        self.advisor_resume = Advisor_History.objects.create(
            advisor_id=self.advisor.id,
            granted_prize="something from some place"
        )
        self.user2 = User.objects.create_user(
            email="a@a.co", password="2",
            phone_number="1234",
            first_name="mammad",
            last_name="mama", is_advisor=False,
            gender="M", year_born=timezone.now(),
            is_active=True,
        )

        self.token = Token.objects.create(user=self.user)
        print(self.token)
        self.api_authentication()

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

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
        response = self.client.put('/api/update-advisor-resume/' + str(self.advisor_resume.id) + '/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_upload_docs(self):
        photo_file = self.generate_photo_file()
        data = {
            'photo': photo_file
        }
        response = self.client.post(f'/api/upload-doc-file/{self.advisor.id}', data, follow=True, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_uploaded_docs(self):
        response = self.client.get(f'/api/upload-doc-file/{self.advisor.id}', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_download_doc_file(self):
        response = self.client.get(f'/api/download-doc-file/{self.advisor_doc.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_doc_file_status_put(self):
        data = {"confirmed_at": True}
        response = self.client.put(f'/api/update-doc-file-status/{self.advisor_doc.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_doc_file_status_patch(self):
        data = {"confirmed_at": True}
        response = self.client.patch(f'/api/update-doc-file-status/{self.advisor_doc.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_profile_image(self):
        response = self.client.get('/api/get-profile-image/' + str(self.user.id))
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

    def test_advisor_can_see_resservation_details(self):
        res = self.client.get('/api/list-advisor-reservation-details/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_advisor_can_see_resservation_details_with_id(self):
        res = self.client.get('/api/list-advisor-reservation-details/' + str(self.user.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_test_user_cannot_update_another_user_profile(self):
    #     data = {
    #         "granted_prize": "blah blah blah"
    #     }
    #     response = self.client.put('/api/update-advisor-resume/'+ str(self.advisor_resume.id) +'/', data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
