from rest_framework.test import APITestCase
from login.models import Reservation, User, Advisor, Advisor_Document, Advisor_History, Rate
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

        self.advisoruser1 = User.objects.create_user(
            email="d@d.co", password="2",
            phone_number="126734",
            first_name="ady",
            last_name="mama", is_advisor=True,
            gender="M", year_born=timezone.now(),
            is_active=True,
            is_staff=False,
        )
        self.advisor1 = Advisor.objects.create(
            is_mental_advisor=True,
            is_family_advisor=False,
            is_sport_advisor=False,
            is_healthcare_advisor=False,
            is_ejucation_advisor=False,
            meli_code="54090084",
            advise_method="on",
            address="shkfjsdkj",
            telephone="55387958",
            user_id=self.advisoruser1.id
        )

        self.rate = Rate.objects.create(
            advisor_id=self.advisor1.id,
            user_id=self.orduser.id,
            text="fkgj",
            rate="3",
        )

        self.tokenadmin = Token.objects.create(user=self.usernotadmin)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenadmin.key)

    def test_not_admin_cant_create_user(self):
        userdata = {
            "email": "a.h@gmail.com",
            "password": "2",
            "phone_number": "1094522",
            "first_name": "aa",
            "gender": "M",
            "year_born": "2021-07-17 08:27:03",
            "last_name": "bb",
            "is_advisor": True
        }

        res = self.client.post('/admin-panel/create-user/', userdata)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_delete_user(self):
        res = self.client.delete('/admin-panel/delete-user/' + str(self.orduser.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_get_user_info(self):
        res = self.client.get('/admin-panel/get-user-info/' + str(self.orduser.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_nto_admin_cant_list_rates(self):
        res = self.client.get('/admin-panel/list-users-rates/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_list_particular_advisor_rates(self):
        res = self.client.get('/admin-panel/list-particular-user-rates/' + str(self.advisor1.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_update_comment_status(self):
        rate_data = {
            "is_confirmed": True
        }
        res = self.client.patch('/admin-panel/delete-or-update-comment-status/' + str(self.rate.id) + '/', rate_data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_get_particular_advisor_info(self):
        res = self.client.get(f'/admin-panel/get-advisor-info/{self.advisor1.id}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_list_advisors_chat(self):
        res = self.client.get(f'/admin-panel/list-advisors-chat/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_get_particular_advisor_chat(self):
        res = self.client.get(f'/admin-panel/retrieve-particular-advisor-chats/{self.advisor1.id}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # def test_not_admin_cant_list_advisors(self):
    #     res = self.client.get(f'/admin-panel/list-advisors/')
    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_admin_cant_delete_rate(self):
        res = self.client.delete('/admin-panel/delete-or-update-comment-status/' + str(self.rate.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    # def test_notadmin_cannot_get_user_info(self):
    #     res = self.client.get('/admin-panel/list-users/')
    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    def test_admin_can_see_reservation_details(self):
        res = self.client.get('/list-reservation-details/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


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

        self.advisoruser1 = User.objects.create_user(
            email="d@d.co", password="2",
            phone_number="126734",
            first_name="ady",
            last_name="mama", is_advisor=True,
            gender="M", year_born=timezone.now(),
            is_active=True,
            is_staff=False,
        )
        self.advisor1 = Advisor.objects.create(
            is_mental_advisor=True,
            is_family_advisor=False,
            is_sport_advisor=False,
            is_healthcare_advisor=False,
            is_ejucation_advisor=False,
            meli_code="54090084",
            advise_method="on",
            address="shkfjsdkj",
            telephone="55387958",
            user_id=self.advisoruser1.id
        )

        self.rate = Rate.objects.create(
            advisor_id=self.advisor1.id,
            user_id=self.orduser.id,
            text="fkgj",
            rate="3",
        )

        self.chat1 = Chat.objects.create(title='as1321')

        self.reservation = Reservation.objects.create(
            chat_id = self.chat1.id,
            user_id = self.orduser.id,
            advisor_user_id = self.advisoruser1.id,
            reservation_datetime = "2023-07-17 08:27:03",
            end_session_datetime = "2023-07-17 10:27:03"
        )

        self.tokenadmin = Token.objects.create(user=self.useradmin)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.tokenadmin.key)

    def test_useradmin_can_create_user(self):
        userdata = {
            "email": "a.h@gmail.com",
            "password": "2",
            "phone_number": "1094522",
            "first_name": "aa",
            "gender": "M",
            "year_born": "2021-07-17 08:27:03",
            "last_name": "bb",
            "is_advisor": True
        }

        res = self.client.post('/admin-panel/create-user/', userdata)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_advisor(self):
        data = {
            "email": "advisor@example.com",
            "first_name": "ali",
            "last_name": "mohammadi",
            "password": "12345678",
            "phone_number": "09356167889",
            "gender": "M",
            "year_born": "2022-05-24 08:27:03",
            "is_advisor": True,
            "is_mental_advisor": True,
            "is_family_advisor": True,
            "is_sport_advisor": True,
            "is_healthcare_advisor": True,
            "is_ejucation_advisor": True,
            "meli_code": "3871584907",
            "advise_method": "b",
            "address": "",
            "telephone": "",
            "email_confirmed_at" : ""
        }

        res = self.client.post('/admin-panel/create-advisors/', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_admin_can_get_particular_advisor_info(self):
        res = self.client.get(f'/admin-panel/get-advisor-info/{self.advisor1.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_list_advisors_chat(self):
        res = self.client.get(f'/admin-panel/list-advisors-chat/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_get_particular_advisor_chat(self):
        res = self.client.get(f'/admin-panel/retrieve-particular-advisor-chats/{self.advisor1.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_admin_can_list_advisors(self):
    #     res = self.client.get(f'/admin-panel/list-advisors/')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)



    def test_admin_can_delete_user(self):
        res = self.client.delete('/admin-panel/delete-user/' + str(self.orduser.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_get_user_info(self):
        res = self.client.get('/admin-panel/get-user-info/' + str(self.orduser.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_list_users(self):
        res = self.client.get('/admin-panel/list-users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_list_rates(self):
        res = self.client.get('/admin-panel/list-users-rates/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_list_particular_advisor_rates(self):
        res = self.client.get('/admin-panel/list-particular-user-rates/' + str(self.advisor1.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_update_rate_status(self):
        rate_data = {
            "is_confirmed": True
        }
        res = self.client.patch('/admin-panel/delete-or-update-comment-status/' + str(self.rate.id) + '/', rate_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_rate(self):
        res = self.client.delete('/admin-panel/delete-or-update-comment-status/' + str(self.rate.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_see_reservation_details(self):
        res = self.client.get('/admin-panel/list-reservation-details/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_reservation(self):
        res = self.client.delete('/admin-panel/delete-reservation/' + str(self.reservation.id) + '/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    
