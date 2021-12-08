from django import forms
from users.models import User
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('this user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('incorrect password')
            if not user.check_password(password):
                raise forms.ValidationError('This user is not active')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
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
        email = self.cleaned_data.get('email')
        password_confirm = self.cleaned_data.get('password_confirm')
        password = self.cleaned_data.get('password')
        same_emails = User.objects.filter(email=email)
        if same_emails.exists():
            raise forms.ValidationError('this email already exists')
        if password != password_confirm:
            raise forms.ValidationError('passwords is not matches')
        return super(UserRegisterForm, self).clean(*args, **kwargs)
