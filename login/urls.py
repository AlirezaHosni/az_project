from django.urls import path
from .views import ListRateByAdvisorIdAPI, BestAdvisorsByProfessionAPI, GetAllAdvisorsAPI, CreateAdvisor, UpdateAdvisorResumeAPI, ListAdvisorResumeAPI,ListRateAPI, CreateRateAPI, SendRequestAPI, AdvisorRequestsInfoAPI, RequestUpdateStatus, RequestsInfoAPI, LoginAPI, SignUpAPI, UserInfoAPI, AdvisorInfoAPI, SearchAdvisorAPI
from knox import views as knox_views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


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
    path('users-comments-by-advisor-id/', ListRateByAdvisorIdAPI.as_view()),
    path('create-comment/', CreateRateAPI.as_view()),
    path('advisor-resume/', ListAdvisorResumeAPI.as_view()),
    path('update-advisor-resume/<int:granted_prize_id>/', UpdateAdvisorResumeAPI.as_view()),
    path('create-advisor/', CreateAdvisor.as_view()),
    path('all-advisors/', GetAllAdvisorsAPI.as_view()),
    path('particular-advisors/', BestAdvisorsByProfessionAPI.as_view()),

    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]
