from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from rest_framework import serializers

from .models import UserProfile

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'age',
                  'account_type',
                  'is_seller',
                  'created_at',
                  'updated_at',
                  'is_seller',
                    )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('id',
                  'email',
                  'password',
                  'is_active',
                  'is_blocked',
                  'is_staff',
                  'is_superuser',
                  'last_login',
                  'created_at',
                  'updated_at',
                  'profile',
                  )

        read_only_fields = ('id',
                            'created_at',
                            'updated_at',
                            'last_login',
                            'is_active',
                            'is_blocked',
                            'is_superuser',
                            'is_staff',
                            'is_superuser',)

        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
        
    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile)
        return user


