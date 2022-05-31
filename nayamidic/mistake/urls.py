from django.urls import path
# from .views import signupfunk
from . import views
from .views import HomeView, PostCreate, Signup, Login, Logout, PostView, UserUpdate, PostEdit, mypagefunk


urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('loout/', Logout.as_view(), name='logout'),
    path('post_create/<int:pk>', PostCreate.as_view(), name='post_create'),
    path('post_view/', PostView.as_view(), name='post_view'),
    path('user_update/<int:pk>', UserUpdate.as_view(), name='user_update'),
    path('post_edit/<int:pk>', PostEdit.as_view(), name='post_edit'),
    path('my_page/<int:pk>', mypagefunk, name='my_page'),

]