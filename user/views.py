from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages

# Create your views here.
from user.forms import CustomUserRegistrationForm


def user_login(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/')
    user_login_form = AuthenticationForm()

    if request.method == 'POST':
        user_login_form = AuthenticationForm(request=request, data=request.POST)
        if user_login_form.is_valid():
            login(request, user_login_form.get_user())
            messages.success(request, 'successful Login')
            return redirect('ecommerce:index')

    return render(request, 'pages/users/login.html', context={'form': user_login_form})


def user_logout(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'successful logout')
        return redirect('user:login')
    return HttpResponse(status=404)


def user_registration(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/')
    user_registration_form = CustomUserRegistrationForm()
    if request.method == 'POST':
        user_registration_form = CustomUserRegistrationForm(request.POST)
        if user_registration_form.is_valid():
            user_registration_form.save()
            messages.success(request, 'Registration completed Successfully!')
            return redirect('user:login')
    return render(request, 'pages/users/register.html', context={'form': user_registration_form})
