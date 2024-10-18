from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny

from apps.users.serializers import UserSerializer

UserModel = get_user_model()

class UserCreateView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserBlockView(GenericAPIView):
    pass


class UserUnblockView(GenericAPIView):
    pass


class UserToManager(GenericAPIView):
    pass


