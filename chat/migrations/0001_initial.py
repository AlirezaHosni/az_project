# Generated by Django 3.2.4 on 2021-12-03 21:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_started', models.DateTimeField(auto_now_add=True)),
                ('time_changed', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(error_messages={'unique': 'هر چت فقط یکبار میتواند ساخته شود'}, max_length=255, unique=True)),
            ],
            options={
                'ordering': ['-time_changed'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats_message', to='chat.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_message', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Chat_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False)),
                ('chat_start_datetime', models.DateTimeField()),
                ('end_session_datetime', models.DateTimeField()),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats_users', to='chat.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_chat', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
