from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from login.models import User, Student
from .models import Questionnaire, Question, Answer
from login.serializer import UserSerializer


class CreateListQuestionnaire(serializers.ModelSerializer): 
    class Meta:
    	model = Questionnaire
    	fields = ['name', 'description']
    
			