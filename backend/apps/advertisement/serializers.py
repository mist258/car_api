from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.car.models import CarModel
from apps.users.serializers import ProfileSerializer

from ..car.serializers import CarModelSerializer
from .models import AdvertisementModel, CarPhotoModel, StatisticAdvertisementModel


class AdvAddCarPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarPhotoModel
        fields = ('car_photo',)

        extra_kwargs = {
            'car_photo':
                {
                    'required': False
                }
        }


class AdvertisementSerializer(serializers.ModelSerializer):
    car_photo = AdvAddCarPhotoSerializer(many=True, read_only=True)
    car = CarModelSerializer()
    seller = ProfileSerializer(read_only=True)

    class Meta:
        model = AdvertisementModel
        fields = ('seller',
                  'id',
                  'price',
                  'currency',
                  'sale_location',
                  'is_active',
                  'car_photo',
                  'car_additional_describe',
                  'car',)

        read_only_fields = ('seller',
                            'id',
                            'is_active',)

    @atomic
    def create(self, validated_data: dict):

        request = self.context.get('request')
        seller = request.user.profile

        if seller.role_type == 'seller':

            if seller.account_type == 'basic':
                advertisement = AdvertisementModel.objects.filter(seller=seller).count()

                if advertisement >= 1:
                    raise ValidationError(_('You should have premium subscription to publish more, then 1 advertisement'))
        else:
            raise ValidationError(_('Only authenticated seller can create advertisement'))

        car_data = validated_data.pop('car',)
        car, created = CarModel.objects.get_or_create(**car_data)

        return AdvertisementModel.objects.create(seller=seller, car=car, **validated_data)


    @atomic
    def update(self, instance, validated_data: dict):
        data = validated_data.pop('car')
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if data:
            car_instance = instance.car
            for key, value in data.items():
                setattr(car_instance, key, value)

        instance.save()
        return instance


class StatisticAdvertisementModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatisticAdvertisementModel
        fields = ('general_views',
                  'day_views',
                  'week_views',
                  'month_views',
                  'last_view_date',
                  'car_avg_price_in_uk',
                  'car_avg_price_in_region',)


class PremiumAdvertisementSerializer(AdvertisementSerializer):
    statistic = StatisticAdvertisementModelSerializer(read_only=True)
    avg_price_in_region = serializers.SerializerMethodField(read_only=True)
    avg_price_in_uk = serializers.SerializerMethodField(read_only=True)

    class Meta(AdvertisementSerializer.Meta):
        model = AdvertisementModel
        fields = AdvertisementSerializer.Meta.fields +(
                  'statistic',
                  'avg_price_in_region',
                  'avg_price_in_uk',
                  )

        read_only_fields = (
                            'avg_price_in_uk',
                            'avg_price_in_region',
                            'statistic',
                            )

    # return avg car's price in a certain region by car_brand and sale_region
    def get_avg_price_in_region(self, object):
        car_brand = object.car.car_brand
        sale_location = object.sale_location
        return AdvertisementModel.avg_price_by_brand_in_region(car_brand, sale_location)

    # return avg car's price in Ukr by car_brand
    def get_avg_price_in_uk(self, object):
        car_brand = object.car.car_brand
        return AdvertisementModel.avg_price_by_region(car_brand)

