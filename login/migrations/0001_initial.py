# Generated by Django 3.2.4 on 2021-07-16 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import login.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(error_messages={'unique': 'کاربری با این شماره تماس از قبل موجود میباشد'}, max_length=11, null=True, unique=True)),
                ('gender', models.CharField(max_length=8, null=True)),
                ('year_born', models.DateTimeField(null=True)),
                ('is_advisor', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', login.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_mental_advisor', models.BooleanField(default=False, null=True)),
                ('is_family_advisor', models.BooleanField(default=False, null=True)),
                ('is_sport_advisor', models.BooleanField(default=False, null=True)),
                ('is_healthcare_advisor', models.BooleanField(default=False, null=True)),
                ('is_ejucation_advisor', models.BooleanField(default=False, null=True)),
                ('meli_code', models.CharField(error_messages={'unique': 'کاربری با این کد ملی از قبل موجود میباشد'}, max_length=10, null=True, unique=True)),
                ('advise_method', models.CharField(choices=[('on', 'online'), ('off', 'offline'), ('b', 'both')], max_length=3, null=True)),
                ('address', models.CharField(max_length=300, null=True, verbose_name='advisor address')),
                ('telephone', models.CharField(max_length=11, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_content', models.TextField(null=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(null=True)),
                ('is_accepted', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_Done', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.advisor')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('rate', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.advisor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Advisor_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('granted_prize', models.CharField(max_length=300)),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.advisor')),
            ],
        ),
    ]