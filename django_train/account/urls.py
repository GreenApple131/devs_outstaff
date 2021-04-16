from django.contrib import admin
from django.urls import path, re_path, include

from . import views


urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
   

    path('staff-only/', views.staff_only, name='staff-only'),
    path('free-access/', views.free_access, name='free-access'),

]