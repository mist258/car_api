from django.urls import path

from .views import AdvertisementCreateView, ShowAllUsersAdvView

urlpatterns = [
    path('/posts', AdvertisementCreateView.as_view(), name='advertisement'),
    path('/listing', ShowAllUsersAdvView.as_view(), name='list-adv' ),
]