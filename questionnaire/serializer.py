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
    questionnaire = QuestionnaireSerializer(read_only=True)
    score = serializers.SerializerMethodField('get_score')

    # @property
    # def score(self, Question):
    #     answer = Answer.objects.filter(Q(user=self.context['request'].user) & Q(question=Question))
    #     if answer.count() == 0:
    #         return -1
    #     return answer.first().score

    class Meta:
        model = Question
        fields = ['id', 'questionnaire', 'description', 'category', 'score', 'created_at',
                  'updated_at']

        read_only_fields = ['id', 'questionnaire', 'category', 'score', 'description', 'created_at', 'updated_at']

    def get_score(self, question):
        answer = Answer.objects.filter(Q(user=self.context['request'].user) & Q(question=question))
        if answer.count() == 0:
            return -1
        return answer.first().score

    # def create(self, validated_data):
    #     questionnaire = get_object_or_404(Questionnaire, id=validated_data.pop('questionnaire_id'))
    #     validated_data['questionnaire'] = questionnaire
    #     return validated_data
    #
    # def update(self, instance, validated_data):
    #     questionnaire = get_object_or_404(Questionnaire, id=validated_data.pop('questionnaire_id'))
    #     validated_data['questionnaire'] = questionnaire
    #     super(QuestionSerializer, self).update(instance, validated_data)
    #     return instance


class Questionnaire_UserSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer(read_only=True)
    questionnaire_id = serializers.IntegerField(write_only=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Questionnaire_User
        fields = ['questionnaire_id', 'questionnaire', 'user', 'total', 'somatization', 'obsessive_compulsive',
                  'interpersonal_sensitivity',
                  'depression', 'anxiety', 'hostility', 'tophobic_anxietytal', 'paranoid_ideation', 'psychoticism'
            , 'other', 'created_at', 'updated_at']
        read_only_fields = ['questionnaire', 'user', 'total', 'somatization', 'obsessive_compulsive',
                            'interpersonal_sensitivity',
                            'depression', 'anxiety', 'hostility', 'tophobic_anxietytal', 'paranoid_ideation',
                            'psychoticism', 'other', 'created_at', 'updated_at']

    def create(self, validated_data):
        questionnaire = get_object_or_404(Questionnaire, id=validated_data.pop('questionnaire_id'))
        validated_data['questionnaire'] = questionnaire

        user = self.context['request'].user
        validated_data['user'] = user

        total = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1)).aggregate(Avg('score'))['score__avg']
        validated_data['total'] = total if total else -1
        somatization = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='somatization')).aggregate(Avg('score'))['score__avg']
        validated_data['somatization'] = somatization if somatization else -1

        obsessive_compulsive = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='obsessive_compulsive')).aggregate(Avg('score'))['score__avg']
        validated_data['obsessive_compulsive'] = obsessive_compulsive if obsessive_compulsive else -1

        interpersonal_sensitivity = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='interpersonal_sensitivity')).aggregate(Avg('score'))['score__avg']
        validated_data['interpersonal_sensitivity'] = interpersonal_sensitivity if interpersonal_sensitivity else -1

        depression = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='depression')).aggregate(Avg('score'))['score__avg']
        validated_data['depression'] = depression if depression else -1

        anxiety = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='anxiety')).aggregate(Avg('score'))['score__avg']
        validated_data['anxiety'] = anxiety if anxiety else -1

        hostility = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='hostility')).aggregate(Avg('score'))['score__avg']
        validated_data['hostility'] = hostility if hostility else -1

        tophobic_anxietytal = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='tophobic_anxietytal')).aggregate(Avg('score'))['score__avg']
        validated_data['tophobic_anxietytal'] = tophobic_anxietytal if tophobic_anxietytal else -1

        paranoid_ideation = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                                          Q(user=user) & Q(score__gt=-1) & Q(
            question__category='paranoid_ideation')).aggregate(Avg('score'))['score__avg']
        validated_data['paranoid_ideation'] = paranoid_ideation if paranoid_ideation else -1

        psychoticism = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='psychoticism')).aggregate(Avg('score'))['score__avg']
        validated_data['psychoticism'] = psychoticism if psychoticism else -1

        other = Answer.objects.filter(Q(question__questionnaire=questionnaire) &
                                  Q(user=user) & Q(score__gt=-1) & Q(question__category='other')).aggregate(Avg('score'))['score__avg']
        validated_data['other'] = other if other else -1







        # validated_data['depression'] = Answer.objects.filter(Q(questionnaire=questionnaire) &
        #                           Q(user=user) & Q(score__gt=-1) & Q(category='depression')).aggregate(Avg('score'))
        # validated_data['anxiety'] = Answer.objects.filter(Q(questionnaire=questionnaire) &
        #                           Q(user=user) & Q(score__gt=-1) & Q(category='anxiety')).aggregate(Avg('score'))
        # validated_data['hostility'] = Answer.objects.filter(Q(questionnaire=questionnaire) &
        #                           Q(user=user) & Q(score__gt=-1) & Q(category='hostility')).aggregate(Avg('score'))
        # validated_data['tophobic_anxietytal'] = Answer.objects.filter(Q(questionnaire=questionnaire) &
        #                           Q(user=user) & Q(score__gt=-1) & Q(category='tophobic_anxietytal')).aggregate(Avg('score'))
        # validated_data['paranoid_ideation'] = Answer.objects.filter(Q(questionnaire=questionnaire) &
        #                           Q(user=user) & Q(score__gt=-1) & Q(category='paranoid_ideation')).aggregate(Avg('score'))
        # validated_data['psychoticism'] = Answer.objects.filter(Q(questionnaire=questionnaire) &
        #                           Q(user=user) & Q(score__gt=-1) & Q(category='psychoticism')).aggregate(Avg('score'))
        # validated_data['other'] = Answer.objects.filter(Q(questionnaire=questionnaire) &
        #                           Q(user=user) & Q(score__gt=-1) & Q(category='other')).aggregate(Avg('score'))
        # instance = super().create(validated_data)
        return validated_data


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(write_only=True, required=False)
    question = QuestionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['question', 'question_id', 'user', 'score', 'created_at', 'updated_at']
        read_only_fields = ['question', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        question = get_object_or_404(Question, id=validated_data.pop('question_id'))
        answer = Answer.objects.filter(Q(user=self.context['request'].user) & Q(question=question))
        validated_data['question'] = question
        user = self.context['request'].user
        validated_data['user'] = user
        if answer.count() == 0:
            super().create(validated_data)
        else:
            instance = answer.first()
            instance.score = validated_data['score']
            instance.save()
        return validated_data

    # def update(self, instance, validated_data):
    #     question = get_object_or_404(Question, id=validated_data.pop('question_id'))
    #     validated_data['question'] = question
    #     user = self.context['request'].user
    #     validated_data['user'] = user
    #     super(AnswerSerializer, self).update(instance, validated_data)
    #     return instance

