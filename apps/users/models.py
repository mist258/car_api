from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from core.models import BaseModel


class UserCustomModel(AbstractUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = "user"
        ordering = ["id"]


class UserProfile(BaseModel):

    ACCOUNT_TYPE = (
        ("premium", "premium"),
        ("basic", "basic"),
    )

    class Meta:
        db_table = "user_profile"
        ordering = ["id"]
