from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Password
from django import forms
from .forms import PasswordForm

@login_required
def password_list(request):
    passwords = Password.objects.filter(user=request.user)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.save(commit=False)
            password.user = request.user
            password.save()
            return redirect('password_list')
    else:
        form = PasswordForm()
    return render(request, 'password/password_list.html', {
        'passwords': passwords,
        'form': form
    })