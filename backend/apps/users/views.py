from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.models import UserProfile
from apps.users.serializers import ProfileSerializer, UserSerializer
from core.permissions.is_superuser_permission import IsSuperUser

UserModel = get_user_model()


class UserCreateView(CreateAPIView): # create new user
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserBlockView(GenericAPIView): # block user
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_active and not user.is_blocked:
            user.is_active = False
            user.is_blocked = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserUnblockView(GenericAPIView): # unblock user
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_blocked and not user.is_active:
            user.is_blocked = False
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToManagerView(GenericAPIView): # make user manager
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_active and not user.is_staff and not user.is_blocked:
            user.is_staff = True
            user.is_seller = False
            user.is_buyer = False
            user.save()

        serializer_user = UserSerializer(user)

        profile = UserProfile.objects.get(user=user)

        if profile.role_type == 'buyer' or profile.role_type == 'seller':
            profile.role_type = 'other'
            profile.save()

        serializer_profile = ProfileSerializer(profile)

        response_data = {
            'user': serializer_user.data,
            'profile': serializer_profile.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class GetMeView(GenericAPIView): # get my info
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
