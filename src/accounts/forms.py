from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password']
        

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Email or Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Email or Phone Number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    