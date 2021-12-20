from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.forms import UserLoginForm, UserRegisterForm
from users.models import User
from users.tokens import account_activation_token


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        user = User.create_user(email, password, first_name, last_name)
        new_user = authenticate(email=user.email, password=password)
        login(request, new_user)
        user.send_confirmation_link(get_current_site(request))
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def confirm_email_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        request.user.is_email_confirmed = True
        request.user.save()
        return render(request, 'accounts/successfully_email_confirmation.html')
    else:
        return render(request, 'accounts/invalid_email_confirmation_link.html')


@login_required
def email_not_confirmed_view(request):
    if not request.user.is_email_confirmed:
        return render(request, 'accounts/email_not_confirmed.html')
    else:
        return redirect('my_profile')


def send_activation_link_view(request):
    if request.method == 'POST':
        current_site = get_current_site(request)
        request.user.send_confirmation_link(current_site)
    return redirect('my_profile')