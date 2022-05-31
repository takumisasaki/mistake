from dataclasses import field
from django.shortcuts import render, redirect, get_object_or_404
from urllib import request
from .models import Post,  User as user
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

class SignupForm(UserCreationForm):
    class Meta:
        model = user
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'categories', 'text')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('username','nickname', 'email', 'id')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        # print("これは送られてきたPOST"+username)
        id = self.instance.id
        name_check = user.objects.exclude(id=id).values('username')
        email_check = user.objects.exclude(id=id).values('email')
        for i in range(len(name_check)):
            for j in name_check[i].values():
                if username == j:
                    self.add_error('username', 'この名前は既に登録されています。')
        for i in range(len(email_check)):
            for j in email_check[i].values():
                if email == j:
                    self.add_error('username', 'このアドレスは既に登録されています。')
        return cleaned_data

    def __init__(self, username=None, nickname=None, email=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        check = user.objects.values('username') 
        for i in range(len(check)):
            for j in check[i].values():
                print(j)
        super().__init__(*args, **kwargs)
        
    
    def update(self, user):
        print(user,'---------')
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.nickname = self.cleaned_data['nickname']
        user.save()

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'categories', 'text')
    
    def __init__(self, user=None, categories=None, text=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        print('最初に呼ばれるインスタンス')
        super().__init__(*args, **kwargs)

    def update(self, post):
        post.user = self.cleaned_data['user']
        post.categories = self.cleaned_data['categories']
        post.text = self.cleaned_data['user']
        post.save()
