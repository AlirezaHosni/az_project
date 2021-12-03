from django.urls import path
from .views import CreateListQuestionnaireAPIView, CreateListQuestionAPIView, CreateListAnswerAPIView, RetrieveUpdateDestroyQuestionAPIView, RetrieveUpdateDestroyAnswerAPIView, RetrieveUpdateDestroyQuestionnaireAPIView




urlpatterns = [

    path('questionnaire/',CreateListQuestionnaireAPIView.as_view()),
    path('questionnaire/<int:id>',RetrieveUpdateDestroyQuestionnaireAPIView.as_view()),
    path('question',CreateListQuestionAPIView.as_view()),
    path('question/<int:id>/',RetrieveUpdateDestroyQuestionAPIView.as_view()),
    path('answer',CreateListAnswerAPIView.as_view()),
    path('answer/<int:id>/',RetrieveUpdateDestroyAnswerAPIView.as_view()),
]