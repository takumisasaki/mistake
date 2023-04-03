import email
from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Emailを入力してください')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります')
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=50, validators=[username_validator], unique=True)
    nickname = models.CharField(_("nickname"), max_length=50)
    email = models.EmailField(_("email_address"),blank=True, null=True, unique=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    image = models.ImageField(upload_to='medi/', blank=True, null=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.CharField(null=True, max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True, help_text='投稿日')
    updated_at = models.DateTimeField(null=True, help_text='編集済み')
    delete_flag = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    post_positive = models.FloatField(null=True, default=None)
    post_negative = models.FloatField(null=True, default=None)
    post_neutral = models.FloatField(null=True, default=None)
    post_mixed = models.FloatField(null=True, default=None)

class like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_flag = models.BooleanField(default=False)
    
class Follow(models.Model):
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

