# Generated by Django 5.1.2 on 2024-10-26 10:25

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import core.services.file_service


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarPhotoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_photo', models.ImageField(blank=True, null=True, upload_to=core.services.file_service.FileService.upload_file)),
            ],
            options={
                'db_table': 'car_photo',
            },
        ),
        migrations.CreateModel(
            name='StatisticAdvertisementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_views', models.IntegerField(default=0)),
                ('day_views', models.IntegerField(default=0)),
                ('week_views', models.IntegerField(default=0)),
                ('month_views', models.IntegerField(default=0)),
                ('last_view_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('car_avg_price_in_region', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('car_avg_price_in_uk', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'statistic_adv',
            },
        ),
        migrations.CreateModel(
            name='AdvertisementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(1)])),
                ('currency', models.CharField(choices=[('USD', 'Usd'), ('UAH', 'Uah'), ('EUR', 'Eur')], max_length=3)),
                ('sale_location', models.CharField(choices=[('vinnytsia', 'Vinnytsia'), ('dnipro', 'Dnipro'), ('donetsk', 'Donetsk'), ('zhytomyr', 'Zhytomyr'), ('zaporizhzhia', 'Zaporizhzhia'), ('ivano-frankivsk', 'Ivano Frankivsk'), ('kyiv', 'Kyiv'), ('kropyvnytskyi', 'Kropyvnytskyi'), ('luhansk', 'Luhansk'), ('lutsk', 'Lutsk'), ('lviv', 'Lviv'), ('mykolaiv', 'Mykolaiv'), ('odesa', 'Odesa'), ('poltava', 'Poltava'), ('rivne', 'Rivne'), ('sumy', 'Sumy'), ('ternopil', 'Ternopil'), ('uzhhorod', 'Uzhhorod'), ('kharkiv', 'Kharkiv'), ('kherson', 'Kherson'), ('khmelnytskyi', 'Khmelnytskyi'), ('cherkasy', 'Cherkasy'), ('chernivtsi', 'Chernivtsi'), ('chernihiv', 'Chernihiv')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('car_additional_describe', models.TextField(max_length=200)),
                ('photo_count', models.IntegerField(default=0)),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='car.carmodel')),
            ],
            options={
                'db_table': 'advertisement',
                'ordering': ['id'],
            },
        ),
    ]
