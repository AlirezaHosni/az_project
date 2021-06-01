from django.db import models

# Create your models here.
class Users(models.Model):
    # ID use a primary key and random
    # car_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)(unique_key=True)
    password = models.CharField(min_length=8)
    email = models.CharField(max_length=100)(unique_key=True)
    phone_number = models.CharField(length=11)(unique_key=True)
    house_number = models.CharField(length=11)
    gender = models.CharField()
    year_born = models.DateTimeField()
    is_advisor = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # picture???
    image = models.ImageField()(null=True, blank = True, upload_to = "images/")
    #for using ImageField you should run this command from the cmd:
    #  pip install pillow