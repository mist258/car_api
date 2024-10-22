from django.core import validators
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from apps.car.models import CarModel
from apps.users.models import UserProfile
from core.models import BaseModel
from core.services.file_service import FileService

from .choices_adv.adv_choices import AdvCurrencyChoices, AdvRegionChoices


class StatisticAdvertisementModel(BaseModel):
    class Meta:
        db_table = "statistic_adv"

    general_views = models.IntegerField(default=0)
    day_views = models.IntegerField(default=0)
    week_views = models.IntegerField(default=0)
    month_views = models.IntegerField(default=0)
    last_view_date = models.DateTimeField(default=timezone.now)
    car_avg_price_in_region = models.DecimalField(max_digits=10,
                                               decimal_places=3,
                                               default=0)
    car_avg_price_in_uk = models.DecimalField(max_digits=10,
                                                decimal_places=3,
                                                default=0)


class AdvertisementModel(models.Model):
    class Meta:
        db_table = "advertisement"
        ordering = ["id"]

    seller = models.ForeignKey(UserProfile,
                               on_delete=models.CASCADE,
                               related_name="seller_profile",)
    car = models.OneToOneField(CarModel, on_delete=models.CASCADE,
                               related_name="car",)
    price = models.DecimalField(max_digits=10,
                                decimal_places=3,
                                blank=False,
                                null=False,
                                validators=[validators.MinValueValidator(1)])
    currency = models.CharField(max_length=3, choices=AdvCurrencyChoices.choices,
                                blank=False,
                                null=False)
    sale_location = models.CharField(choices=AdvRegionChoices.choices,
                                     blank=False,
                                     null=False,
                                     max_length=20)
    is_active = models.BooleanField(default=True)
    car_additional_describe = models.TextField(max_length=200,
                                               blank=False,
                                               null=False)
    statistic = models.OneToOneField(StatisticAdvertisementModel,on_delete=models.CASCADE,
                                     related_name="statistic",
                                     blank=True,
                                     null=True,)


    @classmethod
    def avg_price_by_brand_in_region(cls, car_brand, sale_location):
        avg_price = (
            cls.objects.filter(car__car_brand=car_brand, sale_location=sale_location, is_active=True)
            .aggregate(avg_price=Avg('price'))['avg_price']
        )
        return avg_price or 0

    @classmethod
    def avg_price_by_region(cls, car_brand):
        avg_price = (
            cls.objects.filter(car__car_brand=car_brand, is_active=True)
            .aggregate(avg_price=Avg('price'))['avg_price']
        )
        return avg_price or 0


class CarPhotoModel(BaseModel):
    class Meta:
        db_table = "car_photo"

    car_photo = models.ImageField(upload_to=FileService.upload_file,
                                    blank=True,
                                    null=True)
    adv_car = models.ForeignKey(AdvertisementModel, on_delete=models.CASCADE, related_name="car_photo",)