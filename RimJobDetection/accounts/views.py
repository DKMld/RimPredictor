from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from RimJobDetection.accounts.forms import UserRegistrationForm


@csrf_protect
def register_user(request):
    registration_form = UserRegistrationForm()

    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            user = registration_form.save(commit=True)

            login(request, user)

            return redirect('home page')

    context = {'form': registration_form}
    return render(request, 'account_templates/register_page.html', context)


@csrf_protect
def log_in_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('paswrd')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home page')
        elif user is None:
            messages.error(request, 'Username or password is incorrect!')
            return redirect('login user')

    return render(request, 'account_templates/log_in_page.html')


@csrf_protect
@login_required
def logout_user(request):
    logout(request)
    return redirect('home page')
