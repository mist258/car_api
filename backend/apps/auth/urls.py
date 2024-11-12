from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ActivationUserView, RecoveryPasswordRequestView, RecoveryPasswordView, SocketTokenView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'), # +
    path('/refresh', TokenRefreshView.as_view(), name='token_refresh'), # +
    path('/activate/<str:token>', ActivationUserView.as_view(), name='activate'), # +
    path('/recovery_request', RecoveryPasswordRequestView.as_view(), name='recovery_request'), # +
    path('/recovery_password/<str:token>', RecoveryPasswordView.as_view(), name='recovery_password' ), # +
    path('/socket_token', SocketTokenView.as_view(), name='socket_token'), #
]
