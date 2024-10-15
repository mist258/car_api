# Generated by Django 5.1.2 on 2024-10-15 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advertisement', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisementmodel',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_profile', to='users.userprofile'),
        ),
        migrations.AddField(
            model_name='advertisementmodel',
            name='statistic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistic', to='advertisement.statisticadvertisementmodel'),
        ),
    ]
