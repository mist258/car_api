from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import UserModel, UserSerializer
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken
from drf_yasg.utils import swagger_auto_schema

from .serializers import EmailSerializer, PasswordSerializer

User = get_user_model()

@method_decorator(name='patch', decorator=swagger_auto_schema(security=[], operation_id='activate user'))
class ActivationUserView(GenericAPIView):
    '''
        activate user account
        (for everyone)
    '''
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[], operation_id='recovery password request'))
class RecoveryPasswordRequestView(GenericAPIView):
    '''
        a password reset request
        (for everyone)
    '''
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer  = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        EmailService.recovery(user)
        return Response({'detail': 'check your email'}, status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[], operation_id='recovery password'))
class RecoveryPasswordView(GenericAPIView):
    '''
        recovery password
        (for everyone)
    '''
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        token = kwargs['token']
        user = JWTService.verify_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response({'detail':' your password has been changed'}, status.HTTP_200_OK)
