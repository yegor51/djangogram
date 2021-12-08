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
        return f'{self.first_name} {self.last_name} {self.email}'

    @staticmethod
    def create_user(email, password, first_name, last_name):
        new_user = User(email=email,
                        first_name=first_name,
                        last_name=last_name,
                        )
        new_user.set_password(password)
        new_user.save()
        return new_user

    def edit_profile(self, bio=None, avatar=None, first_name=None, last_name=None):
        if bio is not None:
            self.bio = bio

        if avatar:
            self.avatar = avatar

        if first_name:
            self.first_name = first_name

        if last_name:
            self.last_name = last_name

        self.save()
