from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='static/img/',
                               default='static/default/blank_avatar.png')
    is_email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    @staticmethod
    def create(email, password, first_name, last_name, is_active=True, commit=True):
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