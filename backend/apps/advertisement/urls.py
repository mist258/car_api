from django.urls import path

from .views import AdvertisementCreateView, DestroyUserAdvView, ShowAllUsersAdvView, UpdateUserAdvView

urlpatterns = [
    path('/posts', AdvertisementCreateView.as_view(), name='advertisement'), # +
    path('/listing', ShowAllUsersAdvView.as_view(), name='list-adv' ), # +
    path('/<int:pk>/retrieving', UpdateUserAdvView.as_view(), name='update-adv'), # +
    path('/<int:pk>/destruction', DestroyUserAdvView.as_view(), name='delete-adv'), # +


]