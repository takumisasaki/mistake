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
        fields = ('username', 'nickname', 'email', 'password1', 'password2')
        labels = {
            'username':'user_id', 
            'nickname':'ニックネーム',
            'email':'メールアドレス',
            'password1':'パスワード',
            'password2':'パスワード（確認用）'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "user_creation_form"

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('username','nickname', 'id', 'image')
        labels = {
            'username':'user_id',
            'nickname':'ニックネーム',
            'id':'id',
            'image':'image'
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        id = self.instance.id
        name_check = user.objects.exclude(id=id).values('username')
        return cleaned_data

    def __init__(self, username=None, nickname=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        check = user.objects.values('username')
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "user_creation_form"

        
    def update(self, user):
        print(user,'---------')
        # user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.nickname = self.cleaned_data['nickname']
        user.save()

class PostForm(forms.Form):
    categories = forms.fields.ChoiceField(
        choices = (
            ('仕事', '仕事'),
            ('学校', '学校'),
            ('ギャンブル', 'ギャンブル'),
        ),
        required=True,
        widget=forms.widgets.Select
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '40', 'rows': '10'}),
        label='',
        max_length=150,
        required=True,
    )

class PostEditForm(forms.Form):
    categories = forms.fields.ChoiceField(
        choices = (
            ('仕事', '仕事'),
            ('恋愛', '恋愛'),
            ('友人関係', '友人関係'),
            ('学校', '学校'),
            ('ギャンブル', 'ギャンブル'),
            ('詐欺', '詐欺')
        ),
        required=True,
        widget=forms.widgets.Select
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '40', 'rows': '10'}),
        label='',
        max_length=150,
        required=True,
    )

    user = forms.IntegerField(
        required=True
    )

    post_id = forms.IntegerField(
        required=True
    )
    
    def __init__(self, user, *args, **kwargs):
        # print(kwargs['pk'])
        self.pk = kwargs.pop('pk')
        self.categories = kwargs.pop('categories')
        initial_lst = []
        for i in self.categories:
            initial_lst.append(i.categories)
            initial_lst.append(i.text)
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.fields['categories'].initial = initial_lst[0]
        self.fields['text'].initial = initial_lst[1]

        # kwargs.setdefault('label_suffix', '')

    def update(self, post):
        post_box = Post.objects.get(pk=self.cleaned_data['post_id'])
        human = user.objects.get(pk=self.cleaned_data['user'])
        print(post_box)
        post_box.user = human
        post_box.categories = self.cleaned_data['categories']
        post_box.text = self.cleaned_data['text']
        # print(post.user, post.categories, post.text)
        post_box.save()

# class SampleChoiceForm(forms.Form):
#     choice1 = forms.fields.ChoiceField(
#         choices = (
#             ('ja', '日本'),
#             ('us', 'アメリカ'),
#             ('uk', 'イギリス'),
#             ('ch', '中国'),
#             ('kr', '韓国')
#         ),
#         required=True,
#         widget=forms.widgets.Select
#     )
