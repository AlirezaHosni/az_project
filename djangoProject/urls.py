"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.views import initialize, ContiguousCreate, ContiguousDelete, freeDisk, ChangeBlockSize, IndexCreate, IndexDelete, LinkedCreate, LinkedDelete
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('initialize/', initialize.as_view()),
    path('free-disk/', freeDisk.as_view()),
    path('contiguous/create/', ContiguousCreate.as_view()),
    path('contiguous/delete/', ContiguousDelete.as_view()),
    path('index/create/', IndexCreate.as_view()),
    path('index/delete/', IndexDelete.as_view()),
    path('index/change-block-size/', ChangeBlockSize.as_view()),
    path('linked/create/', LinkedCreate.as_view()),
    path('linked/delete/', LinkedDelete.as_view()),
    path('swagger-ui/', get_swagger_view(title='profile task')),
]
