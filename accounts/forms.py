from django import forms
from users.models import User
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    """
        django form for user login to the site.

        clean functions:
            check that email and password match one of the records in user table.
    """
    email = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))

    def clean(self, *args, **kwargs):
        """check that email and password match one of the records in user table."""
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('email or password do not match')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    """
        django form for user registration in the site.

        fields:
            email - email of the user
            password - password of user
            password_confirm - must be same as the password field
            first_name - first name of user
            last_name - last name of user

        clean functions:
            check that password and password_confirm fields matches.
            check that email not to already in use.
    """
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}),
                               label='set password')
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}),
                                       label='confirm password')
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = User
        fields = ['email',
                  'password',
                  'first_name',
                  'last_name',
                  ]

    def clean(self, *args, **kwargs):
        """check that password and password_confirm fields matches.
            check that email not to already in use."""
        email = self.cleaned_data.get('email')
        password_confirm = self.cleaned_data.get('password_confirm')
        password = self.cleaned_data.get('password')
        same_emails = User.objects.filter(email=email)
        if same_emails.exists():
            raise forms.ValidationError('this email already exists')
        if password != password_confirm:
            raise forms.ValidationError('passwords is not matches')
        return super(UserRegisterForm, self).clean(*args, **kwargs)