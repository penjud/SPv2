from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    betfair_username = forms.CharField(max_length=100, required=True)
    betfair_password = forms.CharField(widget=forms.PasswordInput, required=True)
    betfair_api_key = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'betfair_username', 'betfair_password', 'betfair_api_key')