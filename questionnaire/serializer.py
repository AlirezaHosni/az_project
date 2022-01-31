from django.db import models
from django.db.models import Q, fields, Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from login.models import User
from .models import Questionnaire, Question, Answer, Questionnaire_User
from login.serializer import UserSerializer


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuestionSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer()
    questionnaire_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'questionnaire_id', 'questionnaire', 'description', 'score', 'category', 'created_at',
                  'updated_at']
        read_only_fields = ['id', 'questionnaire', 'created_at', 'updated_at']

    def create(self, validated_data):
        questionnaire = get_object_or_404(Questionnaire, id=validated_data.pop('questionnaire_id'))
        validated_data['questionnaire'] = questionnaire
        return validated_data

    def update(self, instance, validated_data):
        questionnaire = get_object_or_404(Questionnaire, id=validated_data.pop('questionnaire_id'))
        validated_data['questionnaire'] = questionnaire
        super(QuestionSerializer, self).update(instance, validated_data)
        return instance


class Questionnaire_UserSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer(read_only=True)
    questionnaire_id = serializers.IntegerField(write_only=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Questionnaire_User
        fields = ['id', 'questionnaire_id', 'questionnaire', 'user', 'total', 'somatization', 'obsessive_compulsive',
                  'interpersonal_sensitivity',
                  'depression', 'anxiety', 'hostility', 'tophobic_anxietytal', 'paranoid_ideation', 'psychoticism'
            , 'other', 'created_at', 'updated_at']
        read_only_fields = ['id', 'questionnaire', 'user', 'total', 'somatization', 'obsessive_compulsive',
                            'interpersonal_sensitivity',
                            'depression', 'anxiety', 'hostility', 'tophobic_anxietytal', 'paranoid_ideation',
                            'psychoticism', 'other', 'created_at', 'updated_at']

    def create(self, validated_data):
        questionnaire = get_object_or_404(Questionnaire, id=validated_data.pop('questionnaire_id'))
        validated_data['questionnaire'] = questionnaire

        user = get_object_or_404(User, email=self.context['request'].user.email)
        validated_data['user'] = user

        validated_data['total'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1)).aggregate(Avg('score'))
        validated_data['somatization'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='somatization')).aggregate(Avg('score'))
        validated_data['obsessive_compulsive'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='obsessive_compulsive')).aggregate(Avg('score'))
        validated_data['interpersonal_sensitivity'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='interpersonal_sensitivity')).aggregate(Avg('score'))
        validated_data['depression'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='depression')).aggregate(Avg('score'))
        validated_data['anxiety'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='anxiety')).aggregate(Avg('score'))
        validated_data['hostility'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='hostility')).aggregate(Avg('score'))
        validated_data['tophobic_anxietytal'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='tophobic_anxietytal')).aggregate(Avg('score'))
        validated_data['paranoid_ideation'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='paranoid_ideation')).aggregate(Avg('score'))
        validated_data['psychoticism'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='psychoticism')).aggregate(Avg('score'))
        validated_data['other'] = Question.objects.filter(Q(questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(category='other')).aggregate(Avg('score'))
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
        student = get_object_or_404(User, id=validated_data.pop('student_id'))
        validated_data['student'] = student
        return validated_data
