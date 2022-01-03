from django import forms
from .models import Publication, Comment


class CreatePublicationForm(forms.ModelForm):
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
    class Meta():
            model = Comment
            fields = ('text',)
            widgets = {
                'text': forms.Textarea(attrs={'class': "form-control", 'style': 'height:100px'}),
            }