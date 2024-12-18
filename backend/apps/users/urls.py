from django.urls import path

from .views import (
    DownGradeToBasicAccountView,
    GetMeView,
    MakePremiumAccountView,
    ShowAllUsersView,
    UserBlockView,
    UserCreateView,
    UserToManagerView,
    UserUnblockView,
)

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-create'), 
    path('/<int:pk>/block', UserBlockView.as_view(), name='user-block' ),
    path('/<int:pk>/unblock', UserUnblockView.as_view(), name='user-unblock' ),
    path('/<int:pk>/staff', UserToManagerView.as_view(), name='user-to-manager' ),
    path('/my_info', GetMeView.as_view(), name='get-my-info'),
    path('/list_users', ShowAllUsersView.as_view(), name='list-users' ),
    path('/<int:pk>/premium_account', MakePremiumAccountView.as_view(), name='make-premium-account'),
    path('/<int:pk>/basic_account', DownGradeToBasicAccountView.as_view(), name='download-basic-account'),

]
