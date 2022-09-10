from django import forms
from .models import User, Follow


class EditProfileForm(forms.ModelForm):
    """change first_name, last_name, bio, avatar fields of User object"""
    class Meta():
            model = User
            fields = ('first_name', 'last_name', 'bio', 'avatar')
            widgets = {
                'first_name': forms.TextInput(attrs={'class': "form-control"}),
                'last_name': forms.TextInput(attrs={'class': "form-control"}),
                'bio': forms.Textarea(attrs={'class': "form-control"}),
                'avatar': forms.FileInput(attrs={'class': "form-control"},),
            }