from datetime import datetime
from decimal import Decimal

from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import requests
from apps.advertisement.filters import AdvertisementFilter
from apps.advertisement.models import AdvertisementModel, CarPhotoModel
from apps.advertisement.serializers import AdvAddCarPhotoSerializer, AdvertisementSerializer
from apps.users.models import UserProfile
from core.permissions.is_seller import IsUserSeller


class AdvertisementCreateView(CreateAPIView): # create advertisement for auth user

    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated, IsUserSeller )

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        return Response(res_data, status=status.HTTP_201_CREATED)


class ShowAllUsersAdvView(ListAPIView): # authenticated user can list own advertisement

    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsUserSeller,)

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)

        queryset = AdvertisementModel.objects.filter(seller=user_profile).select_related('car',)
        return queryset


class UpdateUserAdvView(UpdateAPIView): # authenticated user can update own advertisement

    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsUserSeller,)

    def put(self, *args, **kwargs):
        data = self.request.data
        adv = self.get_object()
        serializer = self.serializer_class(adv, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        data = self.request.data
        adv = self.get_object()
        serializer = self.serializer_class(adv, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyUserAdvView(DestroyAPIView): # delete adv for seller
    permission_classes = (IsUserSeller,)
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()

    def delete(self, *args, **kwargs):
        adv = self.get_object()

        car = adv.car
        adv.delete()
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShowAdvertisementListView(ListAPIView):  # show all advertisements
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return AdvertisementModel.objects.all().select_related('car', 'seller')


class AdvCarAddPhotoView(GenericAPIView): # seller can add photo
    serializer_class = AdvAddCarPhotoSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsUserSeller,)

    def put(self, *args, **kwargs):
        file_photo = self.request.FILES
        photo_amount = 10
        adv = self.get_object()
        exist_photos = adv.car_photo.count()

        if exist_photos + len(file_photo) > photo_amount:
            raise ValidationError(_(f' You can not add more. Maximum photo is {photo_amount}. You already uploaded {exist_photos} photos'))
        for index in file_photo:
            serializer = AdvAddCarPhotoSerializer(data={'car_photo': file_photo[index]})
            serializer.is_valid(raise_exception=True)
            adv.photo_count += 1
            serializer.save(adv_car=adv)
        adv_serializer = AdvertisementSerializer(adv)
        return Response(adv_serializer.data, status=status.HTTP_200_OK)


class AdvCarRemovePhotoView(DestroyAPIView): # delete photo
    queryset = CarPhotoModel.objects.all()
    permission_classes = (IsUserSeller,)

    def delete(self, *args, **kwargs):
        photo = self.get_object()

        if photo:
            photo.delete()

            return Response(_(f'Photo have been successfully deleted'),status.HTTP_204_NO_CONTENT)

        return Response(_('Photo not found'),status.HTTP_404_NOT_FOUND)

class CurrencyConverterView(GenericAPIView): # convert price
    queryset = AdvertisementModel.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)

    def get_exchange_rates(self):
        res = requests.get(
            f'https://api.privatbank.ua/p24api/exchange_rates?date={
            datetime.now().strftime('%d.%m.%Y')
            }'
        )

        if res.status_code == 200:
            data = res.json()
            rates = {}

            for rate in data['exchangeRate']:
                if rate.get('currency') in ['USD', 'EUR']:
                    rates[rate['currency']] = {
                        'sale': Decimal(str(rate['saleRate'])),
                        'purchase': Decimal(str(rate['purchaseRate'])),
                    }

            return rates

        return None

    def get(self, *args, **kwargs):
        adv = self.get_object()

        rates = self.get_exchange_rates()

        if not rates:
            return Response(_('Failed to get exchange rates'),status.HTTP_404_NOT_FOUND)

        price = adv.price
        original_currency = adv.currency

        exchange_rates = {}

        for curr, rate in rates.items():
            exchange_rates[curr] = {
                "sale": float(rate["sale"]),
                "purchase": float(rate["purchase"]),
            }

        res = {
            "original": {
                "price": float(price),
                "currency": original_currency,
            },
            "converted": {},
            "exchange_rates": exchange_rates
        }

        if original_currency == "UAN":
            res["converted"]["USD"] = float(price/rates["USD"]["sale"])
            res["converted"]["EUR"] = float(price/rates["EUR"]["sale"])

        if original_currency == "EUR":
            price_in_uah = price * rates["EUR"]["purchase"]
            res["converted"]["UAH"] = float(price_in_uah)
            res["converted"]["USD"] = float(price_in_uah/rates["USD"]["sale"])

        if original_currency == "USD":
            price_in_uah = price * rates["USD"]["purchase"]
            res["converted"]["UAH"] = float(price_in_uah)
            res["converted"]["EUR"] = float(price_in_uah/rates["EUR"]["sale"])

        return Response(res)

class ActivateAdvertisementView(UpdateAPIView):
    pass


class DeactivateAdvertisementView(UpdateAPIView):
    pass