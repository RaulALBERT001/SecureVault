from django import forms
from django.contrib.auth.models import User
from .models import Password

class PasswordForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ['title', 'password']