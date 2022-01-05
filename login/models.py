from django import apps
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey



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
    is_active = models.BooleanField(default=True)
    GENDER = [ ('M','male'),('F','female')]
    username = None
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=11, unique=True, null=True,
    error_messages={
            'unique': "کاربری با این شماره تماس از قبل موجود میباشد",
        })
    gender = models.CharField(choices=GENDER,max_length=8, null=True)
    year_born = models.DateTimeField(null=True)
    is_advisor = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    image = models.ImageField(null=True, blank=True, upload_to="images/")
    status = models.CharField(max_length=7, default='offline', choices=(
            ('offline', 'offline'),
            ('online', 'online'))
            )
    # for using ImageField you should run this command from the cmd:
    #  pip install pillow
    objects = Manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (self.image is None or str(self.image) == "") and self.gender == 'F':
            self.image = "images/female-user.png"
            super().save(*args, **kwargs)
        if (self.image is None or str(self.image) == "") and self.gender == 'M':
            self.image = "images/male-user.png"
            super().save(*args, **kwargs)


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
        is_verified = models.BooleanField(default=False, null=True)
        daily_begin_time = models.TimeField(null=True)
        daily_end_time = models.TimeField(null=True)
        objects = models.Manager()


class Request(models.Model):
    receiver = models.ForeignKey("Advisor",  models.CASCADE)
    sender = models.ForeignKey("User" , models.CASCADE)
    request_content = models.TextField(null=True)
    is_checked = models.BooleanField(default=False)
    is_blocked = models.BooleanField(null=True)
    is_accepted = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reservation_datetime = models.DateTimeField()
    duration_min = models.IntegerField()
    end_session_datetime = models.DateTimeField()



class Invitation(models.Model):
    advisor = models.ForeignKey("Advisor",  models.CASCADE)
    student = models.ForeignKey("User" , models.CASCADE)
    invitation_content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Rate(models.Model):
    advisor = models.ForeignKey("Advisor", models.CASCADE)
    user = models.ForeignKey("User", models.CASCADE)
    text = models.CharField(max_length=300)
    rate = models.CharField(max_length=1, choices=(('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')))
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)


class Advisor_History(models.Model):
    advisor = models.ForeignKey("Advisor", on_delete=models.CASCADE)
    granted_prize = models.CharField(max_length=300)



class Advisor_Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    doc_file = models.FileField(null=True, blank=True, upload_to="Documents/")
    confirmed_at = models.DateTimeField(null=True, blank=True)
    advisor = models.ForeignKey("Advisor", on_delete=models.CASCADE, related_name='advisor')


class Student(models.Model):
    studnet_number = models.CharField(max_length=9, unique=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)


class Notifiaction(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='user_notification')
    type = models.CharField(choices=(('i', 'invitation'), ('r', 'request')), max_length=1, null=True)
    contacts = models.ManyToManyField("User", related_name='contacts')
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

class Email_Verification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)


class Reservation(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='useruser')
    advisor_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='advisoruser')
    reservation_datetime = models.DateTimeField()
    end_session_datetime = models.DateTimeField()
    advising_case = models.CharField(choices=(
            ('mental', 'mental'),
            ('family', 'family'),
            ('sport', 'sport'),
            ('healthcare', 'healthcare'),
            ('education', 'education'),
        ), max_length=11, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)