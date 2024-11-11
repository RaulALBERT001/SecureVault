from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(u'Email address already exists.')
        return email

    # Remove o help_text dos campos username, password1 e password2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover help_text dos campos
        self.fields['username'].help_text = None
        self.fields['username'].error_messages = {'unique': ' '}
        self.fields['email'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None