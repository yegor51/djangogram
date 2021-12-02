from django.shortcuts import render
from django.http import HttpResponse
from .models import User, User


def profile(request, id):
    return render(request, 'main/view_profile.html', {
        'user': User.objects.get(id=id),
    })


def publication(request, id):
    return HttpResponse('test2')