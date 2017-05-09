# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):     #继承AbstractUser
    desc = models.TextField(null=True,blank=True)


