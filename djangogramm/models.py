from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    bio = models.TextField()
    avatar = models.ImageField()
    is_email_confirmed = models.BooleanField()


class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    description = models.TextField()
    publication_date = models.DateTimeField()


class Comment(models.Model):
    id = models.AutoField()
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