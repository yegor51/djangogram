from django.db import models
from users.models import User


class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_name = models.CharField(max_length=50, default='None')
    image = models.ImageField(upload_to='static/img/')
    description = models.TextField(blank=True, default='')
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_as_publication')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes_as_publication')

    @staticmethod
    def create_publication(author, publication_name, image, description):
        new_publication = Publication(author=author,
                                      publication_name=publication_name,
                                      image=image,
                                      description=description)
        new_publication.save()
        return new_publication

    def set_mark(self, user, value):
        if value == 'like':
            self.likes.add(user)
            self.dislikes.remove(user)
        elif value == 'dislike':
            self.likes.remove(user)
            self.dislikes.add(user)
        elif value == 'none':
            self.likes.remove(user)
            self.dislikes.remove(user)
        else:
            raise ValueError('Incorrect `value` argument. It must be one of like/dislike/none')

    def __str__(self):
        return self.publication_name


class Comment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)

    @staticmethod
    def create_comment(publication, author, text):
        new_comment = Comment(
            publication=publication,
            author=author,
            text=text,
        )
        new_comment.save()
        return new_comment

    def __str__(self):
        return self.text[:20]