from dataclasses import field
from django.shortcuts import render, redirect, get_object_or_404
from .models import User as user
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

class SignupForm(UserCreationForm):
    # password = forms.CharField(label='password', widget=forms.PasswordInput(), min_length=8)
    class Meta:
        model = user

        fields = ('username', 'email', 'password1', 'password2')

# def loginfunk(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'login.html', {'context':'ログインに失敗しました。'})
#     return render(request, 'login.html')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
    
