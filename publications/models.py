from django.db import models
from users.models import User


class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_name = models.CharField(max_length=50, default='None')
    image = models.ImageField(upload_to='static/img/')
    description = models.TextField(blank=True, default='')
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)


class Comment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)


class Mark(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.BooleanField()

    class Meta:
        unique_together = (("publication", "user"),)