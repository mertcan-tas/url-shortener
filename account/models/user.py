from shortuuid.django_fields import ShortUUIDField

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from account.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    id = ShortUUIDField(length=10,max_length=10,alphabet="123456789",primary_key=True,editable=False)
    name = models.CharField(max_length=255, verbose_name="Name", null=True)
    email = models.EmailField(max_length=150, verbose_name="Email", unique=True)
        
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    
    class Meta:
        ordering = ['email']

    def __str__(self) -> str:
        return self.email