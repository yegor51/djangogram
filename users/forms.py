from django import forms
from .models import User


class EditProfileForm(forms.ModelForm):
    class Meta():
            model = User
            fields = ('first_name', 'last_name', 'bio', 'avatar')
            widgets = {
                'first_name': forms.TextInput(attrs={'class': "form-control"}),
                'last_name': forms.TextInput(attrs={'class': "form-control"}),
                'bio': forms.Textarea(attrs={'class': "form-control"}),
                'avatar': forms.FileInput(attrs={'class': "form-control"},),
            }