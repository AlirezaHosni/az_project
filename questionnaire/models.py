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
    total = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    somatization = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    obsessive_compulsive = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    interpersonal_sensitivity = models.IntegerField(default=-1,
                                                    validators=[MaxValueValidator(5), MinValueValidator(-1)])
    depression = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    anxiety = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    hostility = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    tophobic_anxietytal = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    paranoid_ideation = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    psychoticism = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    other = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.questionnaire.name + '_' + self.user.id

    class Meta:
        ordering = ['-updated_at']


class Question(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    score = models.IntegerField(default=-1, validators=[MaxValueValidator(5), MinValueValidator(-1)])
    category = models.CharField(choices=(
        ('s', 'somatization'),
        ('oc', 'obsessive_compulsive'),
        ('is', 'interpersonal_sensitivity'),
        ('d', 'depression'),
        ('a', 'anxiety'),
        ('h', 'hostility'),
        ('pa', 'phobic_anxiety'),
        ('pi', 'paranoid_ideation'),
        ('p', 'psychoticism'),
        ('o', 'other'),

    ), max_length=2, null=True)
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
    description = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        limit = 50
        return self.description[:limit] + ('...' if len(self.description) > limit else '')

    class Meta:
        ordering = ['-updated_at']
