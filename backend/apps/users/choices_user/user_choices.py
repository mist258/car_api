from django.db import models


class AccountType(models.TextChoices):
    PREMIUM = 'Premium', 'Premium'
    BASIC = 'Basic', 'Basic'

class UserRoleType(models.TextChoices):
    SELLER = 'seller', 'Seller'
    BUYER = 'buyer', 'Buyer'
    OTHER = 'other', 'Other'
