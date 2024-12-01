from decimal import Decimal

from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.advertisement.filters import AdvertisementFilter
from apps.advertisement.models import AdvertisementModel, CarPhotoModel
from apps.advertisement.serializers import (
    AdvAddCarPhotoSerializer,
    AdvertisementSerializer,
    PremiumAdvertisementSerializer,
)
from apps.users.models import UserProfile
from core.permissions.is_seller import IsUserSeller
from core.permissions.is_superuser_or_is_staff import IsSuperUserOrIsStaff
from core.services.currency_service import CurrencyService
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='post', decorator=swagger_auto_schema(operation_id='create ads'))
class AdvertisementCreateView(CreateAPIView):
    '''
        create advertisement
        (for seller)
    '''

    serializer_class = AdvertisementSerializer
    permission_classes = (IsUserSeller,)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        return Response(res_data, status.HTTP_201_CREATED)


@method_decorator(name='get', decorator=swagger_auto_schema(operation_id='all ads with filtering '))
class ShowAllUsersAdvView(ListAPIView):
    '''
        user can see their own advertisements
        (for seller)
    '''
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsAuthenticated, IsUserSeller,)

    def get_serializer_class(self):
        if self.request.user.is_premium:
            return PremiumAdvertisementSerializer
        return AdvertisementSerializer

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)

        queryset = (AdvertisementModel.objects.filter(seller=user_profile).
                    select_related('car', 'seller', 'statistic'))
        return queryset


@method_decorator(name='put', decorator=swagger_auto_schema(operation_id='full update'))
@method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='partial update'))
class UpdateUserAdvView(UpdateAPIView):
    '''
    put:
        user can make full update own advertisement by id
        (for seller)
    patch:
         user can make partial update own advertisement by id
        (for seller)

    '''
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsUserSeller,)

    def put(self, *args, **kwargs):
        data = self.request.data
        adv = self.get_object()
        serializer = self.serializer_class(adv, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        data = self.request.data
        adv = self.get_object()
        serializer = self.serializer_class(adv, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_id='show user\'s advert by id'))
class ShowUserAdvByIdView(RetrieveAPIView):
    '''
        users can show advertisement by id (advert's id)
        (for everyone)
    '''
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.select_related('car', 'seller',).all()
    filterset_class = AdvertisementFilter
    permission_classes = (AllowAny,)

    def retrieve(self, *args, **kwargs):
        adv = self.get_object()
        if adv.statistic:
            adv.statistic.increment_counter(None, adv)

        serializer = self.get_serializer(adv)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='delete', decorator=swagger_auto_schema(operation_id='delete advert'))
class DestroyUserAdvView(DestroyAPIView):
    '''
        seller can destroy own advertisement by id (advert's id)
        (for manager or superuser)
    '''
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsSuperUserOrIsStaff,)

    def delete(self, *args, **kwargs):
        adv = self.get_object()
        car = adv.car
        adv.delete()
        car.delete()
        return Response(status.HTTP_204_NO_CONTENT)


@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_id='show active advert'))
class ShowAdvertisementListView(ListAPIView):
    '''
        show the entire list of ads
        (for everyone)
    '''
    queryset = AdvertisementModel.objects.select_related('car', 'seller').filter(is_active=True)
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    permission_classes = (AllowAny,)


@method_decorator(name='put', decorator=swagger_auto_schema(operation_id='add photos to advert'))
class AdvCarAddPhotoView(GenericAPIView):
    '''
        user can add advertisement photos (advert's id)
        (for seller)
    '''
    serializer_class = AdvAddCarPhotoSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsUserSeller,)

    def put(self, *args, **kwargs):
        file_photo = self.request.FILES
        photo_amount = 10
        adv = self.get_object()
        exist_photos = adv.car_photo.count()

        if exist_photos + len(file_photo) > photo_amount:
            raise ValidationError(_(f'You can not add more. Maximum photo is {photo_amount}. '
                                    f'You already uploaded {exist_photos} photos'))
        for index in file_photo:
            serializer = AdvAddCarPhotoSerializer(data={'car_photo': file_photo[index]})
            serializer.is_valid(raise_exception=True)
            serializer.save(adv_car=adv)
        adv_serializer = AdvertisementSerializer(adv)
        return Response(adv_serializer.data, status.HTTP_200_OK)


@method_decorator(name='delete', decorator=swagger_auto_schema(operation_id='delete photos in advert'))
class AdvCarRemovePhotoView(DestroyAPIView):
    '''
        user can remove advertisement photos (photo's id)
        (for seller)
    '''
    queryset = CarPhotoModel.objects.all()
    permission_classes = (IsUserSeller,)

    def delete(self, *args, **kwargs):
        photo = self.get_object()

        if photo:
            photo.delete()

            return Response(_(f'Photo have been successfully deleted'),status.HTTP_204_NO_CONTENT)

        return Response(_('Photo not found'),status.HTTP_404_NOT_FOUND)


@method_decorator(name='get', decorator=swagger_auto_schema(security=[], operation_id='convert currency'))
class CurrencyConverterView(CurrencyService, GenericAPIView):
    '''
        convert current currency to another currency (advert's id)
        (for everyone)
    '''
    queryset = AdvertisementModel.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny,)

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
                "sale": round(float(rate["sale"]), 2),
                "purchase": round(float(rate["purchase"]), 2),
            }

        res = {
            "original": {
                "price": round(Decimal(price), 2),
                "currency": original_currency,
            },
            "converted": {},
            "exchange_rates": exchange_rates
        }

        if original_currency == "UAN":
            res["converted"]["USD"] = round(Decimal(price/rates["USD"]["sale"]), 2)
            res["converted"]["EUR"] = round(Decimal(price/rates["EUR"]["sale"]), 2)

        if original_currency == "EUR":
            price_in_uah = price * rates["EUR"]["purchase"]
            res["converted"]["UAH"] = round(Decimal(price_in_uah),2)
            res["converted"]["USD"] = round(Decimal(price_in_uah/rates["USD"]["sale"]), 2)

        if original_currency == "USD":
            price_in_uah = price * rates["USD"]["purchase"]
            res["converted"]["UAH"] = round(Decimal(price_in_uah),2)
            res["converted"]["EUR"] = round(Decimal(price_in_uah/rates["EUR"]["sale"]), 2)

        return Response(res)


@method_decorator(name='get', decorator=swagger_auto_schema(operation_id='nonactive adverts'))
class ShowNonActivateAdvertisementView(ListAPIView):
    '''
        show nonactive advert
        (for manager or superuser)
    '''
    queryset = AdvertisementModel.objects.select_related('car', 'seller').filter(is_active=False)
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    permission_classes = (IsSuperUserOrIsStaff,)


@method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='advert deactivation'))
class DeactivateAdvertisementView(UpdateAPIView):
    '''
        deactivation advert (advert's id)
        (for manager)
    '''
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = AdvertisementSerializer

    def patch(self, *args, **kwargs):
        adv = self.get_object()
        if adv.is_active:
            adv.is_active = False
            adv.save()
        serializer = AdvertisementSerializer(adv)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='advert activation'))
class ActivateAdvertisementView(UpdateAPIView):
    '''
        activate nonactive advert (advert's id)
        (for manager)
    '''
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = AdvertisementSerializer

    def patch(self, *args, **kwargs):
        adv = self.get_object()

        if not adv.is_active:
            adv.is_active = True
            adv.save()

        serializer = AdvertisementSerializer(adv)
        return Response(serializer.data, status.HTTP_200_OK)
