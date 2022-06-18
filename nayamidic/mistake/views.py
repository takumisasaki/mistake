from re import template
import this
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from pkg_resources import resource_stream
from .models import Post, like, User as user
from .forms import LoginForm, SignupForm, PostForm, UserUpdateForm, PostEditForm
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

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
    def form_valid(self, form):
        print('def formvaild')
        form.update(user=self.request.user)
        return super().form_valid(form)

    template_name = 'user_update.html'
    form_class = UserUpdateForm
    model = user
    
    def get_success_url(self):
        print('def get_success_url')
        queryset = user.objects.values('username')
        for i in zip(queryset):
            if self.request.user == i:
                print("重複してんだよこの野郎")
        return reverse('user_update', kwargs={'pk': self.kwargs.get('pk')})

class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'post_edit.html'
    form_class = PostEditForm
    model = Post

    def form_valid(self, form):
        form.update(user=self.request.post)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_edit', kwargs={'pk': self.kwargs.get('pk')})

def mypagefunk(request, pk):
    model = list(Post.objects.filter(user=pk, delete_flag=0).all())
    return render(request, 'my_page.html', {'model':model})

class PostList(LoginRequiredMixin, TemplateView):
    template_name = 'toppage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        return context


def likefunc(request, user_id, post_id):
    model = like.objects.filter(user_id=user_id,  post_id=post_id)
    print(model)
    post_box = Post.objects.get(pk=post_id)
    if model.count() == 0:
        like_table = like()
        like_table.user_id = request.user
        like_table.post_id = post_box
        like_table.save()
    else:
        model.delete()
    this_post = like.objects.filter(post_id=post_id).count()
    post_box.like_count = this_post
    post_box.save()
    print(post_box.like_count)
    if request.is_ajax():
        return JsonResponse({'post_list':post_box})
    return render(request, 'toppage.html')






