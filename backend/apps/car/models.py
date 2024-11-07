from datetime import datetime

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.car.choices_car.car_choices import (
    CarBodyTypeChoices,
    CarBrandChoices,
    CarDrivetrainTypeChoices,
    CarFuelTypeChoices,
    CarGearTypeChoices,
)
from core.models import BaseModel
from django_countries.fields import CountryField


class CarModel(BaseModel):

    class Meta:
        db_table = "car"
        ordering = ["id"]

    car_brand = models.CharField(max_length=20, choices=CarBrandChoices.choices,
                                 blank=False, null=False)
    car_model = models.CharField(max_length=20, blank=False, null=False)
    vin_code = models.CharField(unique=True, blank=False, null=False)
    car_body_type = models.CharField(max_length=15, choices=CarBodyTypeChoices.choices,
                                     blank=False, null=False)
    car_gear_type = models.CharField(max_length=20, choices=CarGearTypeChoices.choices,
                                     blank=False, null=False)
    car_fuel_type = models.CharField(max_length=30, choices=CarFuelTypeChoices.choices,
                                     blank=False, null=False)
    car_mileage = models.FloatField(blank=False, null=False,
                                    validators=[validators.MinValueValidator(0)])
    car_engine_displacement = models.FloatField(blank=False, null=False,
                                                validators=[validators.MinValueValidator(0.0)])
    car_drivetrain = models.CharField(max_length=20, blank=False, null=False,
                                      choices=CarDrivetrainTypeChoices.choices,)
    car_year = models.IntegerField(blank=False, null=False,
                                   validators=[validators.MinValueValidator(1950),
                                               validators.MaxValueValidator(datetime.now().year)],
                                   error_messages=_(f'Car\'s year cannot be less than 1950 and more than {datetime.now().year} ' ))
    car_country_origin = CountryField(blank_label=_('Choose country origin'), blank=False, null=False)
    car_accident_history = models.BooleanField(blank=False, null=False)
