from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to='static/img/', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_name = models.CharField(max_length=50, default='None')
    image = models.ImageField(upload_to='static/img/')
    description = models.TextField(null=True)
    publication_date = models.DateTimeField()


class Comment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateTimeField()


class Mark(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.BooleanField()

    class Meta:
        unique_together = (("publication", "user"),)