from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.


def homepage(request):
    context = {}
    return render(request, 'homepage.html', context)
