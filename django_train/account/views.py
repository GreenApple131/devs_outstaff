from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from . import forms, models
from .decorators import unauthenticated_user, allowed_users


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
@transaction.atomic
def profilePage(request):
    # Updating profile
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Account was updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Something went wrong')
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/userpage.html', context)


@allowed_users(allowed_roles=['staff'])
def staff_only(request):
    return render(request, 'account/staff_only.html', {})


def free_access(request):
    return render(request, 'account/free_access.html', {})


@unauthenticated_user
@transaction.atomic
def registerUser(request):
    form = forms.CreateUserForm()
    profile_form = forms.ProfileForm()

    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            # profile_form = forms.ProfileForm(request.POST, instance=request.user.profile)
            # profile_form.save

            # messages.success(request, 'Your profile was updated!')

            return redirect('login')
        else:
            messages.error(request, 'Something went wrong')

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'account/register.html', context)


@unauthenticated_user
def loginUser(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, 'Username or password is incorrect!')

    context = {}
    return render(request, 'account/login.html', context)


def logoutUser(request):

    logout(request)

    return redirect('homepage')
