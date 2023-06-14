from atexit import register
from dataclasses import fields
from rest_framework import serializers
from .models import Post, User
from django.contrib.auth import authenticate

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text']

class MyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid username/password combination.")

            if not user.is_active:
                raise serializers.ValidationError("User is deactivated.")

        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username'] 
    
class HomeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'categories', 'text']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password')
        extra_kwargs = {
            'username': {'label': 'user_id'},
            'nickname': {'label': 'ニックネーム'},
            'email': {'label': 'メールアドレス'},
            'password': {'label': 'パスワード', 'write_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user