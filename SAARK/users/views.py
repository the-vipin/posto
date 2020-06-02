# Create your views here.
import math, random , smtplib
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import UserRegisterform, UserUpdateform, ProfileUpdateform
from django.db.models import Count
from django.views.generic import ListView ,DetailView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView, FormView
from django.views.generic.edit import ModelFormMixin, UpdateView
from itertools import chain
from django.db.models import Q
from django.urls import reverse
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.utils import timezone
import time
from django.urls.base import reverse
from Bloggers.models import Blogger


@login_required
def profile(request):
    blogpages = Blogger.objects.filter(Q(Members=request.user))
    founderblogpages = Blogger.objects.filter(Q(Founder=request.user))
    context = {
        'blogpages' : blogpages,
        'founderblogpages' : founderblogpages
    }
    return render(request, 'profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserRegisterform(request.POST)            
        if form.is_valid():
            user = form.save(commit=False)
            if User.objects.filter(email=user.email, is_active=True).exists():
                essu ='your email is already exists in our database'
                return render(request, 'registration/signup.html',{'form':form, 'essu':essu})
            else:
                if User.objects.filter(email=user.email, is_active=False).exists():
                    User.objects.filter(email=user.email, is_active=False).delete()
                user.is_active = False
                user.save()
                email_subject = 'Posto conformation code'
                message = render_to_string('activate_account.html',{
                'user': user,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()
                context ={
                'user': user,
                'TITLE': 'registration conformation link sended'
                }
                print("mail is sent")
                return render(request,'registration/reg_conf_msg.html', context) 
    else:   
        context = {
            'form': UserRegisterform(),
            'TITLE': 'Signup form'
        }
    return render(request, 'registration/signup.html',context)


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        return HttpResponse('activate link is invalid')

@login_required
def updateprofile(request):
    if request.method == 'POST':
        U_form = UserUpdateform(request.POST, instance=request.user)
        P_form = ProfileUpdateform(request.POST, request.FILES, instance=request.user.profile)
        if U_form.is_valid() and  P_form.is_valid():
            U_form.save()
            P_form.save()
            return redirect('profile')
    else:
        U_form = UserUpdateform(instance=request.user)
        P_form = ProfileUpdateform(instance=request.user.userprofile)

    context = {
        'U_form' : U_form,
        'P_form' : P_form,
        'TITLE': 'Edit Profile'
    }
    return render(request, 'registration/updateprofile.html', context)

#@login_required
#def updateconnections(request):
    #return






