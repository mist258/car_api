from django.db import models


class AccountType(models.TextChoices):
    PREMIUM = 'premium', 'premium'
    BASIC = 'basic', 'basic'

class UserRoleType(models.TextChoices):
    SELLER = 'seller', 'seller'
    BUYER = 'buyer', 'buyer'
    OTHER = 'other', 'other'
