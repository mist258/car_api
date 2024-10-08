from django.db.transaction import atomic

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.car.models import CarModel

from ..car.serializers import CarModelSerializer
from .models import AdvertisementModel, StatisticAdvertisementModel


class AdvertisementSerializer(serializers.ModelSerializer):
    car = CarModelSerializer()

