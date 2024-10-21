from importlib.resources import files

from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.advertisement.filters import AdvertisementFilter
from apps.advertisement.models import AdvertisementModel
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
    queryset = AdvertisementModel.objects.all()
    filterset_class = AdvertisementFilter
    permission_classes = (AllowAny,)


class AdvCarAddPhotoView(GenericAPIView):
    serializer_class = AdvAddCarPhotoSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsUserSeller,)

    def put(self, *args, **kwargs):
        file_photo = self.request.FILES
        adv = self.get_object()
        for index in file_photo:
            serializer = AdvAddCarPhotoSerializer(data={'photo': file_photo[index]})
            serializer.is_valid(raise_exception=True)
            serializer.save(adv=adv)
        adv_serializer = AdvertisementSerializer(adv)
        return Response(adv_serializer.data, status=status.HTTP_200_OK)





class AdvCarRemovePhotoView(DestroyAPIView):
    pass


class ActivateAdvertisementView(UpdateAPIView):
    pass


class DeactivateAdvertisementView(UpdateAPIView):
    pass