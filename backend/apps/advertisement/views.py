from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.advertisement.models import AdvertisementModel
from apps.advertisement.serializers import AdvertisementSerializer
from apps.users.serializers import UserSerializer


class AdvertisementCreateView(CreateAPIView): # create advertisement
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        return Response(res_data, status=status.HTTP_201_CREATED)

class ShowAllUsersAdvView(ListAPIView):
    serializer_class = AdvertisementSerializer
    queryset = AdvertisementModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return AdvertisementModel.objects.filter(pk=pk)
