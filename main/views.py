from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Publication


def profile(request, id):
    return render(request, 'main/view_profile.html', {
        'user': User.objects.get(id=id),
    })


def publication(request, id):
    return render(request, 'main/view_publication.html', {
        'publication': Publication.objects.get(id=id),
    })