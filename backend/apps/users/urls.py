from django.urls import path

from .views import TestEmailView, UserBlockView, UserCreateView, UserToManagerView, UserUnblockView

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-list-create'), # +
    path('/<int:pk>/block', UserBlockView.as_view(), name='user-block' ), # +
    path('/<int:pk>/unblock', UserUnblockView.as_view(), name='user-unblock' ), # +
    path('/<int:pk>/staff', UserToManagerView.as_view(), name='user-to-manager' ), # +
    path('/email', TestEmailView.as_view(), name='test-email' ),

]
