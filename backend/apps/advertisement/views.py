from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.advertisement.serializers import AdvertisementSerializer


class AdvertisementCreateView(CreateAPIView): # create advertisement
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        # user = self.request.user
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        return Response(res_data, status=status.HTTP_201_CREATED)

class ShowAllUsersView(GenericAPIView):
    serializer_class = ...



