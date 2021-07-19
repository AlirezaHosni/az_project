from django.urls import path,include
from .views import ListAdvisorResumeByAdvisorIdAPI, ImageApiView, GetUserImageAPI, ListRateByAdvisorIdAPI, BestAdvisorsByProfessionAPI, GetAllAdvisorsAPI, CreateAdvisor, UpdateAdvisorResumeAPI, ListAdvisorResumeAPI,ListRateAPI, CreateRateAPI, SendRequestAPI, AdvisorRequestsInfoAPI, RequestUpdateStatus, RequestsInfoAPI, LoginAPI, SignUpAPI, UserInfoAPI, AdvisorInfoAPI, SearchAdvisorAPI
from knox import views as knox_views



urlpatterns = [
    path('signup/', SignUpAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('user-profile/', UserInfoAPI.as_view()),
    path('advisor-profile/', AdvisorInfoAPI.as_view()),
    path('search/', SearchAdvisorAPI.as_view()),
    path('user-requests/', RequestsInfoAPI.as_view()),
    path('update-request-status/<int:id>/', RequestUpdateStatus.as_view()),
    path('advisor-requests/', AdvisorRequestsInfoAPI.as_view()),
    path('send-request/', SendRequestAPI.as_view()),
    path('users-comments/', ListRateAPI.as_view()),
    path('users-comments-by-advisor-id/<int:advisor_id>/', ListRateByAdvisorIdAPI.as_view()),
    path('create-comment/', CreateRateAPI.as_view()),
    path('advisor-resume/', ListAdvisorResumeAPI.as_view()),
    path('update-advisor-resume/<int:granted_prize_id>/', UpdateAdvisorResumeAPI.as_view()),
    path('create-advisor/', CreateAdvisor.as_view()),
    path('all-advisors/', GetAllAdvisorsAPI.as_view()),
    path('particular-advisors/<str:profession>/', BestAdvisorsByProfessionAPI.as_view()),
    path('get-user-image/', GetUserImageAPI.as_view()),
    path('get-profile-image/<id>', ImageApiView.as_view()),
    path('advisor-resume-by-advisor-id/<int:advisor_id>/', ListAdvisorResumeByAdvisorIdAPI.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
]
