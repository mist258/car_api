from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from apps.users.manager import UserCustomManager
from core.models import BaseModel


class UserCustomModel(AbstractUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserCustomManager()


class UserProfile(BaseModel):
    class Meta:
        db_table = 'user_profile'
        ordering = ['id']
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    age = models.IntegerField()
    user = models.OneToOneField(UserCustomModel, on_delete=models.CASCADE, related_name='profile')
