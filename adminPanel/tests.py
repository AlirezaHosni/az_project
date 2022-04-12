from rest_framework.test import APITestCase
from login.models import User, Advisor, Advisor_Document, Advisor_History
from chat.models import Chat, Chat_User, Message
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from rest_framework import status



class NotAdminTestCase(APITestCase):
    def setUp(self):
        self.usernotadmin = User.objects.create_user(
            email="a@a.co", password="2",
            phone_number="1234",
            first_name="mammad",
            last_name="mama", is_advisor=False,
            gender="M", year_born=timezone.now(),
            is_active=True,
            is_staff=False,
        )
        self.orduser = User.objects.create_user(
            email="c@c.co", password="2",
            phone_number="123144",
            first_name="sima",
            last_name="mama", is_advisor=False,
            gender="M", year_born=timezone.now(),
            is_active=True,
            is_staff=False,
        )
        
        self.tokenadmin = Token.objects.create(user=self.usernotadmin)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenadmin.key)

    def test_usernotadmin_cannot_create_user(self):
        userdata = {
                "email":"a.h@gmail.com",
                "password":"2",
                "phone_number":"1094522",
                "first_name":"aa",
                "gender":"M",
                "year_born":"2021-07-17 08:27:03",
                "last_name":"bb",
                "is_advisor":True
            }

        res = self.client.post('/admin-panel/create-user/', userdata)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_notadmin_cannot_delete_user(self):

        res = self.client.delete('/admin-panel/delete-user/'+str(self.orduser.id)+'/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_notadmin_cannot_get_user_info(self):
        res = self.client.get('/admin-panel/get-user-info/'+str(self.orduser.id)+'/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # def test_notadmin_cannot_get_user_info(self):
    #     res = self.client.get('/admin-panel/list-users/')
    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTestCase(APITestCase):
    def setUp(self):
        self.useradmin = User.objects.create_user(
            email="b@b.co", password="2",
            phone_number="1234",
            first_name="ali",
            last_name="mama", is_advisor=False,
            gender="M", year_born=timezone.now(),
            is_active=True,
            is_staff=True,
        )
        self.orduser = User.objects.create_user(
            email="c@c.co", password="2",
            phone_number="121434",
            first_name="sima",
            last_name="mama", is_advisor=False,
            gender="M", year_born=timezone.now(),
            is_active=True,
            is_staff=False,
        )
        
        self.tokenadmin = Token.objects.create(user=self.useradmin)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenadmin.key)

    def test_useradmin_can_create_user(self):
        userdata = {
                "email":"a.h@gmail.com",
                "password":"2",
                "phone_number":"1094522",
                "first_name":"aa",
                "gender":"M",
                "year_born":"2021-07-17 08:27:03",
                "last_name":"bb",
                "is_advisor":True
            }

        res = self.client.post('/admin-panel/create-user/', userdata)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_admin_can_delete_user(self):

        res = self.client.delete('/admin-panel/delete-user/'+str(self.orduser.id)+'/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_get_user_info(self):
        res = self.client.get('/admin-panel/get-user-info/'+str(self.orduser.id)+'/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_list_users(self):
        res = self.client.get('/admin-panel/list-users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
