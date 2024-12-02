from django.urls import path

from .views import (
    ActivateAdvertisementView,
    AdvCarAddPhotoView,
    AdvCarRemovePhotoView,
    AdvertisementCreateView,
    CurrencyConverterView,
    DeactivateAdvertisementView,
    DestroyUserAdvView,
    ShowAdvertisementListView,
    ShowAllUsersAdvView,
    ShowNonActivateAdvertisementView,
    ShowUserAdvByIdView,
    UpdateUserAdvView,
)

urlpatterns = [
    path('/posts', AdvertisementCreateView.as_view(), name='advertisement'),
    path('/listing', ShowAllUsersAdvView.as_view(), name='list-adv' ),
    path('/<int:pk>/retrieving', UpdateUserAdvView.as_view(), name='update-adv'),
    path('/<int:pk>/destruction', DestroyUserAdvView.as_view(), name='delete-adv'),
    path('/adv_listing', ShowAdvertisementListView.as_view(), name='adv-list-adv'),
    path('/<int:pk>/photo', AdvCarAddPhotoView.as_view(), name='add-photo'),
    path('/<int:pk>/remove_photo', AdvCarRemovePhotoView.as_view(), name='remove-photo'),
    path('/<int:pk>/currencies_converter', CurrencyConverterView.as_view(), name='currency_converter'),
    path('/<int:pk>/seller_advert', ShowUserAdvByIdView.as_view(), name='seller-advert'),
    path('/non_active_advert', ShowNonActivateAdvertisementView.as_view(), name='non-active-advert'),
    path('/<int:pk>/activate_advert', ActivateAdvertisementView.as_view(), name='activate-advert'),
    path('/<int:pk>/deactivate_advert', DeactivateAdvertisementView.as_view(), name='deactivate-advert'),

]