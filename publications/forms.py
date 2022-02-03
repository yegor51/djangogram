from django import forms
from .models import Publication, Comment


class CreatePublicationForm(forms.ModelForm):
    """Publication create form. fields similar to Publication model fields"""
    class Meta():
            model = Publication
            fields = ('name', 'image', 'description')
            widgets = {
                'name': forms.TextInput(attrs={'class': "form-control"}),
                'description': forms.Textarea(attrs={'class': "form-control"}),
                'image': forms.FileInput(attrs={'class': "form-control",
                                                'style': 'min-height: 100px'}),
            }


class CreateCommentForm(forms.ModelForm):
    """Comment create form. fields similar to Comment model fields"""
    class Meta():
            model = Comment
            fields = ('text',)
            widgets = {
                'text': forms.Textarea(attrs={'class': "form-control", 'style': 'height:100px'}),
            }