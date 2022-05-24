from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from questionnaire.models import Question, Questionnaire, Questionnaire_User, Answer
from login.models import User, Advisor
from rest_framework.authtoken.models import Token


# Create your tests here.

class RegisterUser(APITestCase):

    def setUp(self):
        self.clientUser = User.objects.create_user(
            email="student@gmail.com", password="1",
            phone_number="09351112222",
            first_name="alireza",
            last_name="karimi", is_advisor=False,
            gender="M", year_born=timezone.now(),
            is_active=True,
        )
        self.advisorUser = User.objects.create_user(
            email="advisor@gmail.com", password="1",
            phone_number="09351116223",
            first_name="alireza",
            last_name="karimi", is_advisor=True,
            gender="M", year_born=timezone.now(),
            is_active=True,
        )
        self.advisor = Advisor.objects.create(
            is_mental_advisor=True,
            is_family_advisor=False,
            is_sport_advisor=False,
            is_healthcare_advisor=False,
            is_ejucation_advisor=False,
            meli_code="1234567890",
            advise_method="on",
            address="mashhad",
            telephone="12345678",
            user_id=self.advisorUser.id
        )
        self.questionnaire = Questionnaire.objects.create(
            name='mental health test',
            description='its a test test'
        )
        self.question = Question.objects.create(
            questionnaire=self.questionnaire,
            description='example question',
            category='somatization'
        )
        self.answer = Answer.objects.create(
            question_id=self.question.id,
            user_id=self.clientUser.id,
            score=2
        )
        self.token = Token.objects.create(user=self.clientUser)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_can_start_test_and_fetch_questions(self):
        response = self.client.get('/questionnaire/start-test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_answer_question(self):
        data = {
            "question_id": self.question.id,
            "score": 2
        }
        response = self.client.post('/questionnaire/question', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_finish_test(self):
        data = {
            "questionnaire_id": self.questionnaire.id
        }
        response = self.client.post('/questionnaire/finish-test', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
