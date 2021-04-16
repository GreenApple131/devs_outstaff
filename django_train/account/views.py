from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

from . import forms
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def registerUser(request):
    form = forms.CreateUserForm()

    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        else:
            messages.error(request, 'Something went wrong')

    context = {'form': form}
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




@allowed_users(allowed_roles=['staff'])
def staff_only(request):
    return render(request, 'account/staff_only.html', {})
    

def free_access(request):
    return render(request, 'account/free_access.html', {})