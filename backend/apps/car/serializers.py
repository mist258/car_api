from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import CarModel


def validate_vin_code(value):
    if len(value) > 17:
        raise serializers.ValidationError(_('VIN code must be less than 17 digits'))
    if len(value) < 17:
        raise serializers.ValidationError(_('VIN code must be greater than 17 digits'))


class CarModelSerializer(serializers.ModelSerializer):
    vin_code = serializers.CharField(validators=[validate_vin_code])

    class Meta:
        model = CarModel
        fields = ('id',
                  'car_brand',
                  'car_model',
                  'car_body_type',
                  'car_fuel_type',
                  'vin_code',
                  'car_gear_type',
                  'car_mileage',
                  'car_engine_displacement',
                  'car_drivetrain',
                  'car_year',
                  'car_country_origin',
                  'car_accident_history',
                  )
