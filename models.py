from django.db import models


# Create your models here.
class Users(models.Model):
    # ID use a primary key and random
    user_id = models.IntegerField(max_length=8, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(length=11, unique=True)
    gender = models.CharField()
    year_born = models.DateTimeField()
    is_advisor = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # picture???
    image = models.ImageField()(null=True, blank=True, upload_to="images/")
    # for using ImageField you should run this command from the cmd:
    #  pip install pillow



