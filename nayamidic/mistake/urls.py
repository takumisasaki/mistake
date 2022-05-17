from django.urls import path
# from .views import signupfunk
from . import views
from .views import HomeView, Signup, Login


urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),

]