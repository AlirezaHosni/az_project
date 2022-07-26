# Generated by Django 3.2.4 on 2022-02-21 16:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Questionnaire_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('somatization', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('obsessive_compulsive', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('interpersonal_sensitivity', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('depression', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('anxiety', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('hostility', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('tophobic_anxietytal', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('paranoid_ideation', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('psychoticism', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('other', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.questionnaire')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_questionnaire', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('somatization', 'somatization'), ('obsessive_compulsive', 'obsessive_compulsive'), ('interpersonal_sensitivity', 'interpersonal_sensitivity'), ('depression', 'depression'), ('anxiety', 'anxiety'), ('hostility', 'hostility'), ('phobic_anxiety', 'phobic_anxiety'), ('paranoid_ideation', 'paranoid_ideation'), ('psychoticism', 'psychoticism'), ('other', 'other')], max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.questionnaire')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(-1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
