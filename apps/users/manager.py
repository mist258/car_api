from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, email=None, password=None, **extra_fields):

        if not email:
            raise ValueError("User must have an email address")

        if not password:
            raise ValueError("User must have a password")

