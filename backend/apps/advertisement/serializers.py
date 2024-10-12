from django.db.transaction import atomic

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.car.models import CarModel
from apps.users.serializers import ProfileSerializer

from ..car.serializers import CarModelSerializer
from .models import AdvertisementModel, StatisticAdvertisementModel


class AdvertisementSerializer(serializers.ModelSerializer):
    car = CarModelSerializer()
    seller = ProfileSerializer(read_only=True)
    avg_price_in_region = serializers.SerializerMethodField()
    avg_price_in_uk = serializers.SerializerMethodField()

    class Meta:
        model = AdvertisementModel
        fields = ('id',
                  'price',
                  'currency',
                  'sale_location',
                  'photo',
                  'is_active',
                  'seller',
                  'car_additional_describe',
                  'car',
                  'statistic',
                  'avg_price_in_region',
                  'avg_price_in_uk',
                  )

        read_only_fields = ('seller',
                            'id',
                            'avg_price_in_uk',
                            'avg_price_in_region',
                            'is_active',
                            'statistic',)

        def get_avg_price_in_region(self, object):
            car_brand = object.car.car_brand
            sale_location = object.sale_location
            return AdvertisementModel.avg_price_by_brand_in_region(car_brand, sale_location)

        def get_avg_price_in_uk(self, object):
            car_brand = object.car.car_brand
            return AdvertisementModel.avg_price_by_region(car_brand)

class StatisticAdvertisementModelSerializer(serializers.ModelSerializer):
    seller_profile = ProfileSerializer()

    class Meta:
        model = StatisticAdvertisementModel
        fields = ('general_views',
                  'day_views',
                  'week_views',
                  'month_views',
                  'last_view_date',
                  'car_avg_price_in_uk',
                  'car_avg_price_in_region')
