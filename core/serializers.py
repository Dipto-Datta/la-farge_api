

from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group, Permission




class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','email','password','position']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['email','name']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'email','created_at','updated_at']

class PasswordChangeSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True) # validators=[validate_password]
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')

class GroupSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = Group
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = Permission
        fields = '__all__'


