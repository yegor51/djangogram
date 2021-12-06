from django.shortcuts import render
from django.shortcuts import redirect


def home(request):
    return redirect('users/all/')
