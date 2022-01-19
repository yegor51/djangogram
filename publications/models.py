from django.db import models
from users.models import User


class Publication(models.Model):
    """
    publication model

    fields:
        author: User object, author of publication.
        name: String, header of publication.
        image: Image file.
        description: Text, description of publication.
        publication_date: DateTime, publication creation time, filled automatically.
        likes: ManyToMany with User model, publication count of likes.
        dislikes: ManyToMany with User model, publication count of dislikes.

    methods:
        create: create new publication.
        set_like: set like to publication.
        set_dislike: set dislike to publication.
        remove_any_mark: remove like and dislike from publication.

    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='None')
    image = models.ImageField(upload_to='static/img/')
    description = models.TextField(blank=True, default='')
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_as_publication')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes_as_publication')

    @staticmethod
    def create(author, name, image, description, commit=True):
        """
        create new publication.

        params:
            author: User object, author of publication.
            name: String, header of publication.
            image: Image file.
            description: Text, description of publication.
            commit: boolean, save this publication if true.

        returns: new publication.
        """
        new_publication = Publication(author=author,
                                      name=name,
                                      image=image,
                                      description=description)
        if commit:
            new_publication.save()
        return new_publication

    def set_like(self, user):
        """
        set like to publication from this user and remove dislike.

        params:
            user: User object.
        """
        self.likes.add(user)
        self.dislikes.remove(user)

    def set_dislike(self, user):
        """
        set dislike to publication from this user and remove like.

        params:
            user: User object.
        """
        self.likes.remove(user)
        self.dislikes.add(user)

    def remove_any_mark(self, user):
        """
        remove like and dislike to publication from this user.

        params:
            user: User object.
        """
        self.likes.remove(user)
        self.dislikes.remove(user)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    comment model

    fields:
        publication: Publication object.
        author: User object, author of comment.
        text: Text, main text of comment.
        publication_date: DateTime, Time of comment creation, filled automatically.

    methods:
        create: create a comment.
    """
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)

    @staticmethod
    def create(publication, author, text, commit=True):
        """
        create Comment object

        params:
            publication: Publication object.
            author: User object, author of comment.
            text: Text, main text of comment.
            commit: Boolean, save comment object if true.

        returns: Comment object.
        """
        new_comment = Comment(
            publication=publication,
            author=author,
            text=text,
        )

        if commit:
            new_comment.save()
        return new_comment

    def __str__(self):
        return self.text[:20]