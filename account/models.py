from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)


class Ngo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class People(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class Needy(models.Model):
    needy_id = models.AutoField(primary_key=True)
    people_id = models.ManyToManyField(People)
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    city = models.CharField(max_length=50, default= 'City')
    state = models.CharField(max_length=50, default= 'State')
    pin = models.CharField(max_length=30, default= 'Pin')
    photo = models.ImageField(blank = 'True', null = 'True', upload_to = "images/")
    status=models.CharField(max_length=11,default='Approach')


class Forms(models.Model):
    forms_id = models.AutoField(primary_key=True)
    user_id = models.ManyToManyField(People)
    needy_id = models.ManyToManyField(Needy)

class Blogs(models.Model):
    blog_id = models.AutoField(primary_key=True)
    ngo_id = models.ManyToManyField(Ngo)
    title = models.CharField(max_length=100, default='Title')
    body = models.CharField(max_length=100000, default = 'hey')
    created_at = models.DateTimeField(default = datetime.now, blank = True)


class solved_cases(models.Model):
    solved_id = models.AutoField(primary_key=True)
    ngo_name = models.CharField(max_length=100, default='Ngo')
    user_name = models.CharField(max_length=100, default='Person')
    needy_name = models.CharField(max_length=100, default='Needy')
    solved_at = models.DateTimeField(default = datetime.now, blank = True)
    user_id = models.ManyToManyField(People)
    ngo_id = models.ManyToManyField(Ngo)
    needy_id = models.ManyToManyField(Needy)


class Leaderboard(models.Model):
    chart_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default='Person Name')
    user_id = models.ManyToManyField(People)
    count = models.IntegerField(default=0)
    date = models.DateField()


    