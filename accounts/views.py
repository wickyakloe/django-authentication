from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts import forms


# Create your views here.
def index(request):
    """Return the index.html file"""
    return render(request, 'index.html')


@login_required(login_url="index")
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('index'))


def login(request):
    """Log the user in"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = forms.UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have sucessfully logged in!")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None,
                                     "Your username or password is incorrect")
    else:
        login_form = forms.UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})


def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = forms.UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register you account at this time")
    else:
        registration_form = forms.UserRegistrationForm()

    return render(request, 'registration.html', {
                  "registration_form": registration_form})


def user_profile(request):
    """The users Profile page"""
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"profile": user})
