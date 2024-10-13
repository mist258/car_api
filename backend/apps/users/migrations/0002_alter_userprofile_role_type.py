# Generated by Django 5.1.2 on 2024-10-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role_type',
            field=models.CharField(choices=[('seller', 'Seller'), ('buyer', 'Buyer'), ('other', 'Other')], max_length=6),
        ),
    ]
