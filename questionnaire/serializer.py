from django.db import models
from django.db.models import Q, fields
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from login.models import User, Student
from .models import Questionnaire, Question, Answer
from login.serializer import UserSerializer


class QuestionnaireSerializerr(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    class Meta:
        model = Questionnaire
        fields = ['id', 'name', 'description', 'creator', 'created_at', 'updated_at']
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']


    def create(self, validated_data):
    	creator = get_object_or_404(User,email=self.context['request'].user.email)
    	validated_data['creator'] = creator
    	return validated_data
   

   
class QuestionSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer()
    questionnaire_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Question
        fields = ['id', 'questionnaire_id', 'questionnaire', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'questionnaire', 'created_at', 'updated_at']


    def create(self, validated_data):
        questionnaire = get_object_or_404(Questionnaire, id=validated_data.pop('questionnaire_id'))
        validated_data['questionnaire'] = questionnaire
        return validated_data



class AnswerSerializer(serializers.ModelSerializer):
    
    question_id = serializers.IntegerField(write_only=True, required=False)
    question = QuestionSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True, required=False)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['question', 'question_id', 'student', 'student_id', 'description', 'name', 'created_at', 'updated_at']
        read_only_fields = ['question', 'student', 'created_at', 'updated_at']


    def create(self, validated_data):
        question = get_object_or_404(Question, id=validated_data.pop('question_id'))
        validated_data['question'] = question
        student = get_object_or_404(Student, id=validated_data.pop('student_id'))
        validated_data['student'] = student
        return validated_data
 