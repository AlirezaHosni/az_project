from django.urls import path,include
from .views import ListAdvisorResumeByAdvisorIdAPI, ImageApiView, GetUserImageAPI, ListRateByAdvisorIdAPI, BestAdvisorsByProfessionAPI, GetAllAdvisorsAPI, CreateAdvisor, UpdateAdvisorResumeAPI, ListAdvisorResumeAPI,ListRateAPI, CreateRateAPI, SendRequestAPI, AdvisorRequestsInfoAPI, RequestUpdateStatus, RequestsInfoAPI, LoginAPI, SignUpAPI, UserInfoAPI, AdvisorInfoAPI, SearchAdvisorAPI
from knox import views as knox_views



urlpatterns = [
        path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
