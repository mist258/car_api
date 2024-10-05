from django.contrib.auth.models import UserManager as Manager


class UserCustomManager(Manager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')

        if not password:
            raise ValueError('Password must be set')


        # normalize email
        email = self.normalize_email(email)
        # create user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # save user
        user.save(using=self._db)
        return user


    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields['is_staff']is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields['is_superuser'] is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields['is_active'] is not True:
            raise ValueError('Superuser must have is_active=True.')

        user = self.create_user(email, password, **extra_fields)
        return user

