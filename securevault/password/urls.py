from django.contrib import admin
from django.urls import path,include 
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("", password_list, name = 'password_list'),
    
]