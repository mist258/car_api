from django.urls import path

from .views import AdvertisementCreateView

urlpatterns = [
    path('/posts', AdvertisementCreateView.as_view(), name='advertisement'),
]