from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login


class UserRegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '******'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '******'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'zeynabyousefi1380@gmail.com'}))
    password_01 = forms.CharField(label='password',
                                  widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}))
    password_02 = forms.CharField(label='confirm password',
                                  widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exist')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this email already exist')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        user = User.objects.filter(password=password).exists()
        if user:
            raise ValidationError('this email already exist')
        return password

    def clean(self):
        cd = super().clean()
        password_01 = cd.get('password_01')
        password_02 = cd.get('password_02')
        if password_02 and password_01 and password_01 != password_02:
            raise ValidationError("password must match")


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '******'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'zeynabyousefi1380@gmail.com'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}))
