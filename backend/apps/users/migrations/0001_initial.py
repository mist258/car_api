# Generated by Django 5.1.2 on 2024-10-09 03:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.users.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCustomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. '
                                                                        'A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set',
                                                  related_query_name='user',
                                                  to='auth.group',
                                                  verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True,
                                                            help_text='Specific permissions for this user.',
                                                            related_name='user_set',
                                                            related_query_name='user',
                                                            to='auth.permission',
                                                            verbose_name='user permissions')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'auth_user',
                'ordering': ['id'],
            },
            managers=[
                ('objects', apps.users.manager.UserCustomManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('first_name', models.CharField(error_messages='First name is invalid',
                                                max_length=50,
                                                validators=[django.core.validators.RegexValidator(regex='^[A-Za-z]*$')])),
                ('last_name', models.CharField(error_messages='Last name is invalid',
                                               max_length=50,
                                               validators=[django.core.validators.RegexValidator(regex='^[A-Za-z]*$')])),
                ('phone_number', models.CharField(error_messages='Phone number is invalid',
                                                  max_length=20,
                                                  validators=[django.core.validators.RegexValidator
                                                              (regex='^\\+?3?8?(0[\\s\\.-]\\d{2}[\\s\\.-]\\d{3}[\\s\\.-]\\d{2}[\\s\\.-]\\d{2})$')])),
                ('age', models.IntegerField(error_messages='Age must be between 18 and 90',
                                            validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(90)])),
                ('is_seller', models.BooleanField(default=False)),
                ('account_type', models.CharField(choices=[('basic', 'basic'), ('premium', 'premium')], default='basic', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
                'ordering': ['id'],
            },
        ),
    ]
