from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.manager import UserCustomManager
from core.models import BaseModel

from .choices_user.user_choices import AccountType, UserRoleType


class UserCustomModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserCustomManager()


class UserProfile(BaseModel):

    class Meta:
        db_table = 'user_profile'
        ordering = ['id']

    first_name = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^[A-Za-z]*$')],
                                  error_messages=_('First name is invalid'))
    last_name = models.CharField(max_length=50, validators=[RegexValidator(regex=r'^[A-Za-z]*$')],
                                                                error_messages=_('Last name is invalid'))
    phone_number = models.CharField(max_length=20, validators=[RegexValidator
                                                               (regex=r'^\+380\d{9}$')],
                                    error_messages=_('Phone number is invalid'))
    age = models.IntegerField(validators=[validators.MinValueValidator(18), validators.MaxValueValidator(90)],
                              error_messages=_('Age must be between 18 and 90'))
    role_type = models.CharField(max_length=6, choices=UserRoleType.choices)
    account_type = models.CharField(max_length=7, choices=AccountType.choices, default='basic')
    user = models.OneToOneField(UserCustomModel, on_delete=models.CASCADE, related_name='profile')
