from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters

UserModel = get_user_model()


class UserFilter(filters.FilterSet):

    class Meta:
        model = UserModel
        fields = ['is_blocked', 'is_active','is_buyer', 'is_seller', 'is_premium']

        is_seller = filters.BooleanFilter(field_name='is_seller')
        is_buyer = filters.BooleanFilter(field_name='is_buyer')
        is_premium = filters.BooleanFilter(field_name='is_premium')
        is_active = filters.BooleanFilter(field_name='is_active')
        is_blocked = filters.BooleanFilter(field_name='is_blocked')
