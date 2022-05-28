from re import template
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Post, User as user
from .forms import LoginForm, SignupForm, PostForm, UserUpdateForm
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class Signup(CreateView):
    template_name = "signup.html"
    model = user
    form_class = SignupForm
    def form_valid(self, form):
        username = self.request.POST.get('username')
        queryset = user.objects.values('username')
        for i in queryset:
            if username == i:
                print("被ってるよ")
                return redirect('signup')
        return super().form_valid(form)
    success_url = reverse_lazy('login')

class Login(LoginView):
    template_name = "login.html"
    form_class = LoginForm


class HomeView(LoginRequiredMixin, TemplateView):#「LoginRequiredMixin → TemplateView」この順番で記述しないとログイン必須機能が表れないので注意！！
    template_name = 'home.html'
    login_url = '/login/'

class Logout(LogoutView):
    template_name = 'logout.html'

class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('home')

class PostView(LoginRequiredMixin, ListView):
    template_name = 'post_view.html'
    model = Post

class UserUpdate(LoginRequiredMixin, UpdateView):    
    print('-------Views')
    def form_valid(self, form):
        print('def formvaild')
        form.update(user=self.request.user)
        return super().form_valid(form)

    template_name = 'user_update.html'
    form_class = UserUpdateForm
    model = user
    studentModel = {'userModel': user.objects.all()}

    
    def get_success_url(self):
        print('def get_success_url')
        queryset = user.objects.values('username')
        for i in zip(queryset):
            if self.request.user == i:
                print("重複してんだよこの野郎")
        return reverse('user_update', kwargs={'pk': self.kwargs.get('pk')})
