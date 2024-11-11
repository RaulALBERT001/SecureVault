from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage   
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.urls import reverse


def index(request):

    messages_to_display = messages.get_messages(request)
    return render(request, 'index.html', {'messages_to_display': messages_to_display})





def register_user(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.active = False
            user.save()
            
            currente_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('registration/account_active_email.html', {
                "user": user,
                'domain': currente_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request,  "Please confirm your email address to complete the registration")
            return redirect('index')
    
    return render(request, 'registration/register.html', {'form': form})



def activate(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect(reverse('index'))
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect(reverse('index'))
    
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect(reverse('index'))
