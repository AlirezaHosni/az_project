from django.db import models
from login.models import Student, User

class Questionnaire(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questionnaire_creator")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']


class Question(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        limit = 50
        return self.description[:limit] + ('...' if len(self.description) > limit else '')

    class Meta:
        ordering = ['-updated_at']


class Answer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_answer")
    description = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        limit = 50
        return self.description[:limit] + ('...' if len(self.description) > limit else '')

    class Meta:
        ordering = ['-updated_at']
