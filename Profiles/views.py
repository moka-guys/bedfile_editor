from django.shortcuts import render, redirect
from django.http import HttpResponse
from Profiles.models import *
import datetime
import requests, sys
import pandas as pd

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from Profiles.forms import SignUpForm, AccountAuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.http import JsonResponse
import re
from django.conf import settings

# Create your views here.
def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your BED MAKER Account'
            message = render_to_string('Profiles/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = signup_form.cleaned_data.get('email').lower()
            send_mail(subject, message, settings.SENDER_EMAIL, [email], fail_silently=False)
            return redirect('account_activation_sent')
        else:
            print(signup_form.errors)
    else:

        signup_form = SignUpForm()
    return render(request, 'Profiles/signup.html', {'form': signup_form})

def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Profile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'Profiles/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'Profiles/account_activation_sent.html')



def logout_view(request):
	logout(request)
	return redirect("home")


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated: 
        return redirect("home")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            
            if user.is_active:
              
                login(request, user)
      
                if destination:
                    return redirect(destination)
                return redirect("home")
            else:
                return redirect('account_not_activated')	
        else:
            return redirect('wrong_password_entered')
				
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "Profiles/login.html", context)

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Profile.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Profiles/password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.SENDER_EMAIL , [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid header found.')
                    return redirect ("password_reset_done")
            else: 
                return redirect('email_not_recognised')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="Profiles/password_reset_table.html", context={"password_reset_form":password_reset_form})
