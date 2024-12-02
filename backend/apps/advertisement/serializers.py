from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.car.models import CarModel
from better_profanity import profanity
from core.services.email_service import EmailService
from core.services.profanity_service import CheckProfanityService

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

    class Meta:
        model = AdvertisementModel
        fields = (
                  'id',
                  'price',
                  'currency',
                  'sale_location',
                  'is_active',
                  'car_photo',
                  'car_additional_description',
                  'car',)

        read_only_fields = (
                            'id',
                            'is_active')

    @atomic
    def create(self, validated_data: dict):
        request = self.context['request']
        seller = request.user.profile

        if seller.account_type == 'basic':
            advertisement = AdvertisementModel.objects.filter(seller=seller).count()
            if advertisement >= 1:
                raise ValidationError(_('You should have premium subscription to publish more, '
                                        'then 1 advertisement'))

        car_data = validated_data.pop('car',)
        car, created = CarModel.objects.get_or_create(**car_data)
        description = validated_data.get('car_additional_description',)

        if profanity.contains_profanity(description):

            advert = AdvertisementModel.objects.create(seller=seller,
                                                       car=car,
                                                       is_active=False,
                                                       **validated_data)

            EmailService.notify_admin(advert, description)

            raise ValidationError(_(f"You will not be able to publish the advertisement using inappropriate language '{description}'. "
                                    f"Please edit it. "
                                    f"A notification about the use of inappropriate language has been sent to the administrator." ))

        statistic = StatisticAdvertisementModel.objects.create()
        advert = AdvertisementModel.objects.create(seller=seller,
                                                   car=car,
                                                   is_active=True,
                                                   statistic=statistic,
                                                   **validated_data)
        return advert


    @atomic
    def update(self, instance, validated_data: dict):
        data = validated_data.pop('car')
        description = validated_data.get('car_additional_description',)

        CheckProfanityService.check_profanity(instance, description)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if data:
            car_instance = instance.car
            for key, value in data.items():
                setattr(car_instance, key, value)

        instance.save()
        return instance


class StatisticAdvertisementModelSerializer(serializers.ModelSerializer):
    last_view_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = StatisticAdvertisementModel
        fields = ('general_views',
                  'day_views',
                  'week_views',
                  'month_views',
                  'last_view_date',)

# serializer for premium account
class PremiumAdvertisementSerializer(AdvertisementSerializer):
    statistic = StatisticAdvertisementModelSerializer(read_only=True)
    avg_price_in_region = serializers.SerializerMethodField(read_only=True)
    avg_price_in_uk = serializers.SerializerMethodField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if not request.user == instance.seller.user:
            data.pop('statistic')
            data.pop('avg_price_in_region')
            data.pop('avg_price_in_uk')

        return data


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

