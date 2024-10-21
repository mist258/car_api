from django.urls import path

from .views import GetMeView, UserBlockView, UserCreateView, UserToManagerView, UserUnblockView

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-create'), # +
    path('/<int:pk>/block', UserBlockView.as_view(), name='user-block' ), # +
    path('/<int:pk>/unblock', UserUnblockView.as_view(), name='user-unblock' ), # +
    path('/<int:pk>/staff', UserToManagerView.as_view(), name='user-to-manager' ), # +
    path('/my_info', GetMeView.as_view(), name='get-my-info') # +

]
