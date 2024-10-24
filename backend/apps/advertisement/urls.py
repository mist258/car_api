from django.urls import path

from .views import (
    AdvCarAddPhotoView,
    AdvCarRemovePhotoView,
    AdvertisementCreateView,
    DestroyUserAdvView,
    ShowAdvertisementListView,
    ShowAllUsersAdvView,
    UpdateUserAdvView,
)

urlpatterns = [
    path('/posts', AdvertisementCreateView.as_view(), name='advertisement'), # +
    path('/listing', ShowAllUsersAdvView.as_view(), name='list-adv' ), # +
    path('/<int:pk>/retrieving', UpdateUserAdvView.as_view(), name='update-adv'), # +
    path('/<int:pk>/destruction', DestroyUserAdvView.as_view(), name='delete-adv'), # +
    path('/adv_listing', ShowAdvertisementListView.as_view(), name='adv-list-adv'), # +
    path('/<int:pk>/photo', AdvCarAddPhotoView.as_view(), name='add-photo'), # +
    path('/<int:pk>/remove_photo', AdvCarRemovePhotoView.as_view(), name='remove-photo'), # +

]