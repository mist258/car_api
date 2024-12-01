from django.db import models


class AccountType(models.TextChoices):
    BASIC = 'basic', 'basic'
    PREMIUM = 'premium', 'premium'

class UserRoleType(models.TextChoices):
    SELLER = 'seller', 'seller'
    BUYER = 'buyer', 'buyer'
    OTHER = 'other', 'other'
