# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AppUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = [field.name for field in model._meta.fields ] 
               

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = AppUser
        fields = [field.name for field in model._meta.fields]
        # fields.append(UserChangeForm.Meta.fields)