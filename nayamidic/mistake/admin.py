from dataclasses import field
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User, Post, like, Follow

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'nickname')

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields':('email', 'password', 'username', 'nickname')}),
        (_('Permission'), {'fields':('is_active', 'is_staff', 'is_superuser',
                            'groups', 'user_permissions')}),
        (_('important dates'), {'fields':('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes':('wide'),
            'fields':('email', 'password1', 'password2'),
        }),
    )

    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username','email', 'is_staff', 'nickname')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'nickname')
    ordering = ('username',)

admin.site.register(User, MyUserAdmin)
admin.site.register(Post)
admin.site.register(like)
admin.site.register(Follow)