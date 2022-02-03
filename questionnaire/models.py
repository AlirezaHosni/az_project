from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from login.models import User


class Questionnaire(models.Model):
    name = models.CharField(max_length=255)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questionnaire_creator")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']


class Questionnaire_User(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_questionnaire")
    total = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    somatization = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    obsessive_compulsive = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    interpersonal_sensitivity = models.IntegerField(default=-1,
                                                    validators=[MaxValueValidator(4), MinValueValidator(-1)])
    depression = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    anxiety = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    hostility = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    tophobic_anxietytal = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    paranoid_ideation = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    psychoticism = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    other = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questionnaire.name + '_' + self.user.id

    class Meta:
        ordering = ['-updated_at']


class Question(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=[
        ('somatization', 'somatization'),
        ('obsessive_compulsive', 'obsessive_compulsive'),
        ('interpersonal_sensitivity', 'interpersonal_sensitivity'),
        ('depression', 'depression'),
        ('anxiety', 'anxiety'),
        ('hostility', 'hostility'),
        ('phobic_anxiety', 'phobic_anxiety'),
        ('paranoid_ideation', 'paranoid_ideation'),
        ('psychoticism', 'psychoticism'),
        ('other', 'other'),

    ], max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        limit = 50
        return self.description[:limit] + ('...' if len(self.description) > limit else '')

    class Meta:
        ordering = ['-updated_at']


class Answer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_answer")
    score = models.IntegerField(default=-1, validators=[MaxValueValidator(4), MinValueValidator(-1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
