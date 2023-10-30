from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Role(models.Model):
    name=models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class User(AbstractUser):
    name=models.CharField(max_length=150)
    username=models.CharField(max_length=150)
    email=models.CharField(max_length=150,unique=True)
    position = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email



