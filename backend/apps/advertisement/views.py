from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.advertisement.serializers import AdvertisementSerializer


class AdvertisementCreateView(GenericAPIView):
    serializer_class = AdvertisementSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        return Response(res_data, status=status.HTTP_201_CREATED)



