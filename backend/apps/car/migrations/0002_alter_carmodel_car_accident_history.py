# Generated by Django 5.1.2 on 2024-11-07 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='car_accident_history',
            field=models.BooleanField(),
        ),
    ]
