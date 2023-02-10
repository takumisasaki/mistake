from dataclasses import field
from multiprocessing import context
from re import template
import this
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView, FormView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from pkg_resources import resource_stream
from .models import Post, Follow, like, User as user
from .forms import LoginForm, SignupForm, PostForm, UserUpdateForm, PostEditForm
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django import forms
from collections import defaultdict
from django.db.models import Q 


class Signup(CreateView):
    template_name = "templates/signup.html"
    model = user
    form_class = SignupForm
    def form_valid(self, form):
        username = self.request.POST.get('username')
        queryset = user.objects.values('username')
        for i in queryset:
            if username == i:
                print("重複してます。")
                return redirect('signup')
        return super().form_valid(form)
    success_url = reverse_lazy('toppage')

class Login(LoginView):
    template_name = "templates/login.html"
    form_class = LoginForm

class HomeView(LoginRequiredMixin, TemplateView):#「LoginRequiredMixin → TemplateView」この順番で記述しないとログイン必須機能が表れないので注意！！
    template_name = 'templates/home.html'
    # login_url = '/login/'

class Logout(LogoutView):
    template_name = 'templates/logout.html'

class PostList(TemplateView):
    template_name = 'templates/toppage.html'
    login_url = '/login/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = []
        #ログインしていない場合 or フォロー数が０の場合 or フォローしているユーザーの総投稿数が０の場合は最新の投稿を表示する
        # ログインしていてフォローしているユーザいる＆投稿数が１以上の場合はフォローしているユーザーの投稿を表示する。
        if(self.request.user.id == None) or len(list(Follow.objects.filter(following=self.request.user)\
            .values_list('followed', flat=True))) == 0:
            context['post_list'].append(Post.objects.filter(delete_flag=0).all().order_by('-created_at'))
        else:
            followed_user = list(Follow.objects.filter(following=self.request.user).values_list('followed', flat=True))
            for i in range(len(followed_user)):
                context['post_list'].append(Post.objects.filter(user=followed_user[i],delete_flag=0).all())
                context['count'] = Follow.objects.values('followed')
        context['recome_user'] = user.objects.all()[:5]
        return context

class SearchListView(ListView):
    template_name = 'templates/post_search.html'
    model = Post
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET.get('q')
        queryset = queryset.filter(delete_flag=0).all()
        if query:
            queryset = queryset.filter(
                Q(categories__icontains=query) | Q(text__icontains=query), delete_flag=0
            )

        return queryset.order_by('-created_at')
        
class PostCreate(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'templates/post_create.html', context)
    
    def post(self, request, pk):
        post_user = request.user
        categories = request.POST.get('categories')
        text = request.POST.get('text')
        post_create = Post()
        post_create.user = post_user
        post_create.categories = categories
        post_create.text = text
        post_create.save()
        return redirect('toppage')

class PostEdit(LoginRequiredMixin, FormView):
    template_name = 'templates/post_edit.html'
    form_class = PostEditForm
    model = Post

    def form_valid(self, form):
        # print(form)
        form.update(form)
        return super().form_valid(form)
    
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        kwgs["pk"] = self.kwargs['pk']
        kwgs['user'] = self.request.user
        kwgs['categories'] = Post.objects.filter(id=kwgs["pk"]).all()
        return kwgs

    def get_success_url(self):
        return reverse('my_page', kwargs={'pk': self.request.user.id })

def deletefunc(request, pk):
    if request.method == 'POST':
        target_post = Post.objects.filter(pk=pk).get(delete_flag=0)
        target_post.delete_flag = 1
        target_post.save()
        id = request.user.id
        model = list(Post.objects.filter(user=id, delete_flag=0).all())
        print(id)
        return render(request, 'templates/my_page.html', {'model':model, 'pk':pk})

class PostView(LoginRequiredMixin, ListView):
    template_name = 'templates/post_view.html'
    model = Post

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) # Article.objects.all() と同じ結果
        # is_publishedがTrueのものに絞り、titleをキーに並び変える
        queryset = queryset.filter(delete_flag=0)

        return queryset

class UserUpdate(LoginRequiredMixin, UpdateView):
    def form_valid(self, form):
        print('def formvaild')
        form.update(user=self.request.user)
        return super().form_valid(form)

    template_name = 'templates/user_update.html'
    form_class = UserUpdateForm
    model = user
    
    def get_success_url(self):
        print('def get_success_url')
        queryset = user.objects.values('username')
        return reverse('user_update', kwargs={'pk': self.kwargs.get('pk')})

def mypagefunk(request, pk):
    model = list(Post.objects.filter(user=pk, delete_flag=0).all())
    iam = user.objects.get(pk=pk)
    followed = Follow.objects.filter(followed_id=pk).all().count()
    following = Follow.objects.filter(following_id=pk).all().count()
    return render(request, 'templates/my_page.html', {'model':model, 'iam':iam, 'followed':followed, 'following':following })

class RecomeView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/recome_user.html'
    model = user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = user.objects.all()[:5]
        print(context['query'])
        return context


def likefunc(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        model = like.objects.filter(user_id=request.user,  post_id=post_id)
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
        context = {
            'post_id':post_box.id,
            'like_count':post_box.like_count
        }
        if request.is_ajax():
            return JsonResponse(context)
        return render(request, 'templates/toppage.html', context)

class FollowView(View):
    template_name = 'templates/follow.html'
    model = Follow
    def post(self, request):
        if request.method == 'POST':
            print(request)
            target_pk = request.POST.get('f_user')
            obj = user.objects.get(pk=target_pk)
            # followed = フォローされたほう
            # following = フォローしたほう
            model = Follow.objects.filter(followed=target_pk, following=request.user)
            print(model.count())
            if model.count() == 0:
                follow_table = Follow()
                follow_table.followed = obj
                follow_table.following = request.user
                follow_table.save()
            else:
                model.delete()
            context = {
                'target_pk' : target_pk,
                'followed_count' : Follow.objects.filter(followed=target_pk).count(),
                'following_count' : Follow.objects.filter(following=target_pk).count(),
            }
        if request.is_ajax():
            return JsonResponse(context)
        return render(request, 'templates/toppage.html')

class UserDetail(LoginRequiredMixin, ListView):
    template_name = 'templates/user_detail.html'
    model = User
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        followed_count = Follow.objects.filter(followed=self.kwargs['pk']).count()
        following_count = Follow.objects.filter(following=self.kwargs['pk']).count()
        detail_user = user.objects.get(pk=self.kwargs['pk'])
        context['followed'] = followed_count
        context['followind'] = following_count
        context['post'] = Post.objects.filter(user=self.kwargs['pk'])
        context['detail_user'] = detail_user

        return context
