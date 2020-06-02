from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Userprofile, Connetions
from django.conf import settings

class UserRegisterform(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name', 'password1', 'password2']

class UserUpdateform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name']

class ProfileUpdateform(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['image','Bio']

class ConnectionUpdateform(forms.ModelForm):
    class Meta:
        model = Connetions
        fields = ['Phone','instagram','FaceBook','Linkdin','YouTube','Twitter','TikTok','Website','Blogs','YourQuotes']
    
