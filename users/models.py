from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class User(AbstractUser):
    """
    user model, inherited from django AbstractUser model.

    fields:
        first_name: String, first name of user.
        last_name: String, last name of user.
        email: String, email address of user.
        bio: text, some information about user.
        avatar: Image, avatar of user.
        is_email_confirmed: Boolean, some functions is not available for user, if email not confirmed.

    methods:
        create: create User object.
        edit_profile: change some fields of User object.
        send_activation_link: send email confirmation link to user email.
    """
    username = None

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='static/img/',
                               default='static/img/blank_avatar_vuwwgx.png')
    is_email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    @staticmethod
    def create(email, password, first_name, last_name, is_active=True, commit=True):
        """
        create new User object.

        params:
            first_name: String, first name of user.
            last_name: String, last name of user.
            email: String, email address of user.
            bio: text, some information about user.
            avatar: Image, avatar of user.
            commit: Boolean, save user object if true.

        returns: new User object.
        """
        new_user = User(email=email,
                        first_name=first_name,
                        last_name=last_name,
                        is_active=is_active
                        )
        new_user.set_password(password)
        if commit:
            new_user.save()
        return new_user

    def edit_profile(self, bio=None, avatar=None, first_name=None, last_name=None):
        """
        change some fields of User object.

        params:
            bio: Text, optional, new bio of user.
            avatar: Image, optional, new avatar of user.
            first_name: String, optional, new first name of user.
            last_name: String, optional, new last name of user.
        """
        if bio is not None:
            self.bio = bio

        if avatar:
            self.avatar = avatar

        if first_name:
            self.first_name = first_name

        if last_name:
            self.last_name = last_name

        self.save()

    def send_confirmation_link(self, current_site):
        """
         send email confirmation link to user email.
        """
        mail_subject = 'Activate your account.'
        message = render_to_string('users/confirm_email_massage_template.html', {
            'user': self,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': account_activation_token.make_token(self),
        })
        email = EmailMessage(
            mail_subject, message, to=[self.email]
        )
        email.send()

    def check_user_followed(self, following):
        return Follow.objects.filter(follower=self, following=following).exists()

    def followings(self):
        return User.objects.filter(id__in=Follow.objects.filter(follower=self).values_list('following'))


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ["follower", "following"]

    @staticmethod
    def create(follower, following, commit=True):
        new_follow = Follow(follower=follower, following=following)

        if commit:
            new_follow.save()

        return new_follow
