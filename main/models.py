from django.db import models


# Create your models here.

class Disk(models.Model):
    isFull = models.BooleanField(default=False)
    file_name = models.CharField(null=True, max_length=255)


class Statistic(models.Model):
    method = models.CharField(max_length=255, unique=True)
    average_time = models.DecimalField(max_length=10, max_digits=6, decimal_places=4, default=0)
    average_waste_space = models.DecimalField(max_length=10, max_digits=6, decimal_places=4, default=0)
    times = models.IntegerField(default=0)
    config = models.JSONField(null=True)


class Index(models.Model):
    file_name = models.CharField(max_length=255)
    index = models.IntegerField(default=0)
    block_size = models.IntegerField(default=0)


class Linked(models.Model):
    file_name = models.CharField(max_length=255)
    index = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    next = models.IntegerField(default=0)
