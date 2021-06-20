from django.urls import path
from .views import LoginAPI, SignUpAPI, UserInfoAPI, AdvisorInfoAPI
from knox import views as knox_views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('signup/', SignUpAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('user-profile/', UserInfoAPI.as_view()),
    path('advisor-profile/', AdvisorInfoAPI.as_view()),

    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]
