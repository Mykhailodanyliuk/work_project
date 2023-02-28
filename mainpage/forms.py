from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Ім'я користувача",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Підтвердження пароля",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    email = forms.EmailField(label="Імейл",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
