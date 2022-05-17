from re import template
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import User as user
from .forms import LoginForm, SignupForm
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class Signup(CreateView):
    # form = SignupForm()
    # context = {'form':form}
    def form_valid(self, form):
        username = self.request.POST.get('username')
        queryset = user.objects.all()
        for i in queryset:
            if username == i.nickname:
                print("被ってるよ")
                return redirect('signup')
        return super().form_valid(form)
    template_name = "signup.html"
    model = user
    form_class = SignupForm
    success_url = reverse_lazy('login')

class Login(LoginView):
    template_name = "login.html"
    form_class = LoginForm

class HomeView(LoginRequiredMixin, TemplateView):#「LoginRequiredMixin → TemplateView」この順番で記述しないとログイン必須機能が表れないので注意！！
    template_name = 'home.html'
    login_url = '/login/'



# def signupfunk(request):
#     if request.method == 'POST':
#         username = request.POST['nickname']
#         password = request.POST['password']
#         try:
#             user = User.objects.create_user(username, '', password)
#             return redirect('login')
#         except IntegrityError:
#             return render(request, 'signup.html', {'error':'このユーザはすでに登録されています'})
#     return render(request, 'login.html')

# class Login(request):


# Create your views here.