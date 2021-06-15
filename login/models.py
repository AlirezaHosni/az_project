from django.db import models
from django.contrib.auth.models import AbstractUser




# Create your models here.
class User(AbstractUser):
   
    username = models.CharField(max_length=100,null=True, default=None)
    email = models.EmailField(unique=True,
    error_messages={
            'unique': "A user with that email already exists.",
        },)
    phone_number = models.CharField(max_length=11, unique=True, null=True)
    gender = models.CharField(max_length=8, null=True)
    year_born = models.DateTimeField(null=True)
    is_advisor = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    # picture???
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    # for using ImageField you should run this command from the cmd:
    #  pip install pillow

    
