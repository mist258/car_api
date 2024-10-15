from apps.car.choices_car.car_choices import (
    CarBodyTypeChoices,
    CarBrandChoices,
    CarDrivetrainTypeChoices,
    CarFuelTypeChoices,
    CarGearTypeChoices,
)
from django_filters import rest_framework as filters

from .choices_adv.adv_choices import AdvCurrencyChoices, AdvRegionChoices
from .models import AdvertisementModel


class AdvertisementFilter(filters.FilterSet):

    class Meta:
        model = AdvertisementModel
        fields = ['price', 'sale_location']

    #  advertisement
    price_range = filters.RangeFilter(field_name='price')
    sale_location = filters.ChoiceFilter(field_name='sale_location', choices=AdvRegionChoices)
    currency = filters.ChoiceFilter(field_name='currency', choices=AdvCurrencyChoices)

    #  car
    car_year_range = filters.RangeFilter(field_name='car__car_year')
    car_brand = filters.ChoiceFilter(field_name='car__car_brand', choices=CarBrandChoices)
    car_body_type = filters.ChoiceFilter(field_name='car__car_body_type', choices=CarBodyTypeChoices)
    car_fuel_type = filters.ChoiceFilter(field_name='car__car_fuel_type', choices=CarFuelTypeChoices)
    car_gear_type = filters.ChoiceFilter(field_name='car__car_gear_type', choices=CarGearTypeChoices)
    car_drivetrain = filters.ChoiceFilter(field_name='car__car_drivetrain', choices=CarDrivetrainTypeChoices)
    car_country_origin = filters.CharFilter(field_name='car__car_country_origin', lookup_expr='icontains')
    car_model = filters.CharFilter(field_name='car__car_model', lookup_expr='icontains')
    car_mileage = filters.RangeFilter(field_name='car__car_mileage')
    car_engine_displacement = filters.RangeFilter(field_name='car__car_engine_displacement')
    car_accident_history = filters.BooleanFilter(field_name='car__car_accident_history')
    order = filters.OrderingFilter(
        fields=(
            'price',
            'car_year',
            'car_brand',
            'car_mileage',
            'car_engine_displacement',
        )
    )

