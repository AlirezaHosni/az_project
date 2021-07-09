from django import apps
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



class Manager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model( email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user( email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
   
    username = None
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=11, unique=True, null=True,
    error_messages={
            'unique': "کاربری با این شماره تماس از قبل موجود میباشد",
        })
    gender = models.CharField(max_length=8, null=True)
    year_born = models.DateTimeField(null=True)
    is_advisor = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    # picture???
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    # for using ImageField you should run this command from the cmd:
    #  pip install pillow
    objects = Manager()

class Advisor(models.Model):
        user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='user')
        is_mental_advisor = models.BooleanField(default=False, null=True)
        is_family_advisor = models.BooleanField(default=False, null=True)
        is_sport_advisor = models.BooleanField(default=False, null=True)
        is_healthcare_advisor = models.BooleanField(default=False, null=True)
        is_ejucation_advisor = models.BooleanField(default=False, null=True)
        meli_code = models.CharField(max_length=10, unique=True, null=True,
                                     error_messages={
                                         'unique': "کاربری با این کد ملی از قبل موجود میباشد",
                                     })
                                     
        advise_method = models.CharField(choices=(
            ('on', 'online'),
            ('off', 'offline'),
            ('b', 'both'),
        ), max_length=3, null=True)

        address = models.CharField("advisor address", max_length=300, null=True)

        telephone = models.CharField(max_length=11, null=True)

        objects = models.Manager()


class Request(models.Model):
    receiver = models.ForeignKey("Advisor",  models.CASCADE)
    sender = models.ForeignKey("User" , models.CASCADE)
    request_content = models.TextField(null=True)
    is_checked = models.BooleanField(default=False)
    is_blocked = models.BooleanField(null=True)
    is_accepted = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_Done = models.BooleanField(default=False)
    
