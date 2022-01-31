from django.db.models import Q
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializer import QuestionnaireSerializer, QuestionSerializer, AnswerSerializer, Questionnaire_UserSerializer
# from .permissions import 
from .models import Questionnaire, Question, Answer


class CreateListQuestionnaireAPIView(generics.ListCreateAPIView):
    serializer_class = QuestionnaireSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyQuestionnaireAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionnaireSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        obj = get_object_or_404(Questionnaire, id=self.kwargs.get('id'))
        # self.check_object_permissions(self.request, obj)
        return obj


class CreateListQuestionAPIView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyQuestionAPIView(generics.UpdateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        obj = get_object_or_404(Question, id=self.kwargs.get('id'))
        # self.check_object_permissions(self.request, obj)
        return obj


class CreateListQuestionnaire_UserAPIView(generics.ListCreateAPIView):
    serializer_class = Questionnaire_UserSerializer
    permission_classes = [IsAuthenticated]


class CreateListAnswerAPIView(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyAnswerAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        obj = get_object_or_404(Answer, id=self.kwargs.get('id'))
        # self.check_object_permissions(self.request, obj)
        return obj
