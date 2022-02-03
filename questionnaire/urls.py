from django.urls import path
from .views import CreateListQuestionnaireAPIView, ListQuestionAPIView, CreateListQuestionnaire_UserAPIView, \
    CreateAnswerAPIView, RetrieveUpdateDestroyAnswerAPIView, RetrieveUpdateDestroyQuestionnaireAPIView

urlpatterns = [

    # path('questionnaire/', CreateListQuestionnaireAPIView.as_view()),
    # path('questionnaire/<int:id>', RetrieveUpdateDestroyQuestionnaireAPIView.as_view()),
    path('start-test', ListQuestionAPIView.as_view()),
    path('question', CreateAnswerAPIView.as_view()),
    path('finish-test', CreateListQuestionnaire_UserAPIView.as_view()),
    # path('answer/<int:id>/', RetrieveUpdateDestroyAnswerAPIView.as_view()),
]
