from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.models import UserProfile
from apps.users.serializers import ProfileSerializer, UserSerializer
from core.permissions.is_superuser_or_is_staff import IsSuperUserOrIsStaff
from core.permissions.is_superuser_permission import IsSuperUser
from drf_yasg.utils import swagger_auto_schema

from .filters import UserFilter

UserModel = get_user_model()

@method_decorator(name='post', decorator=swagger_auto_schema(security=[], operation_id='create user'))
class UserCreateView(CreateAPIView):
    '''
        users registration
        (for everyone)
    '''
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


@method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='block user'))
class UserBlockView(GenericAPIView):
    '''
        block user (
        for manager or superuser)
    '''
    permission_classes = (IsSuperUserOrIsStaff,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id)

    @swagger_auto_schema(responses={status.HTTP_200_OK : UserSerializer()})
    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_active and not user.is_blocked:
            user.is_active = False
            user.is_blocked = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='unblock user'))
class UserUnblockView(GenericAPIView):
    '''
        unblock user
        (for manager or superuser)
    '''
    permission_classes = (IsSuperUserOrIsStaff,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id)

    @swagger_auto_schema(responses={status.HTTP_200_OK : UserSerializer()})
    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if user.is_blocked and not user.is_active:
            user.is_blocked = False
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='patch', decorator=swagger_auto_schema(operation_id='create manager'))
class UserToManagerView(GenericAPIView):
    '''
        make user a manager
        (for superuser)
    '''
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id)

    @swagger_auto_schema(responses={status.HTTP_200_OK : UserSerializer()})
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


@method_decorator(name='get', decorator=swagger_auto_schema(operation_id='about me'))
class GetMeView(GenericAPIView):
    '''
        user can see own info
        (for authenticated users)
    '''
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='get', decorator=swagger_auto_schema(operation_id='show all users'))
class ShowAllUsersView(ListAPIView):
    '''
        show all users
        (for manager or superuser)
    '''
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = (IsSuperUserOrIsStaff,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.id).select_related('profile')
