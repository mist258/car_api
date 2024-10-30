from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.car.models import CarModel
from apps.users.serializers import ProfileSerializer
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
                  'car_additional_description',
                  'edit_attempts',
                  'car',)

        read_only_fields = ('seller',
                            'id',
                            'is_active',
                            'edit_attempts')


    @atomic
    def create(self, validated_data: dict):
        request = self.context.get('request')
        seller = request.user.profile

        if seller.role_type == 'seller':

            if seller.account_type == 'basic':
                advertisement = AdvertisementModel.objects.filter(seller=seller).count()

                if advertisement >= 1:
                    raise ValidationError(_('You should have premium subscription to publish more, '
                                            'then 1 advertisement'))
        else:
            raise ValidationError(_('Only authenticated seller can create advertisement'))

        car_data = validated_data.pop('car', {})
        description = validated_data.get('car_additional_description', '')
        car, created = CarModel.objects.get_or_create(**car_data)


        if profanity.contains_profanity(description):
            remaining = 2 - validated_data.get('edit_attempts', 0)

            if remaining <= 0:
                raise ValidationError(_('Maximum edit attempts reached. '
                                        'Advertisement sent for review.'))
            validated_data['edit_attempts'] = validated_data.get('edit_attempts', 0) + 1
            advert = AdvertisementModel.objects.create(seller=seller,
                                                       car=car,
                                                       is_active=False,
                                                       **validated_data)

            EmailService.notify_admin(advert, description)

            raise ValidationError(_(f'Inappropriate content detected. {remaining} attempts remaining.'))

        statistic = StatisticAdvertisementModel.objects.create()
        advert = AdvertisementModel.objects.create(seller=seller,
                                                   car=car,
                                                   is_active=True,
                                                   statistic=statistic,
                                                   **validated_data)
        return advert

    @atomic
    def update(self, instance, validated_data: dict): # todo -> incorrect validation
        data = validated_data.pop('car')
        description = validated_data.get('car_additional_description', '')

        CheckProfanityService.check_profanity(instance, description)

        if instance.edit_attempts >= 3:
            raise ValidationError(_('Editing not allowed due to excessive profanity attempts.'))

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
