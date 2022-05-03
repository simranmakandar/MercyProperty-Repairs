from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, help_text='Required')
    last_name = forms.CharField(max_length=20, help_text='Required')
    email = forms.EmailField(max_length=60, help_text='Required')

    # address = forms.CharField(max_length=70, help_text='Required')
    # city = forms.CharField(max_length=50, help_text='Required')
    # zipcode = forms.CharField(max_length=10)
    # phone = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
