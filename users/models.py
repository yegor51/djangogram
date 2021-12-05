from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager


class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='static/img/',
                               default='static/default/blank_avatar.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
