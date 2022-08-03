from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from api.filters import RentOfferFiler, SellOfferFiler
from api.models import RentOffer, SellOffer
from api.serializers import RentOfferSerializer, SellOfferSerializer


class SellOfferViewSet(ListAPIView):
    serializer_class = SellOfferSerializer
    filter_backends = (DjangoFilterBackend, )
    queryset = SellOffer.objects.all()
    filterset_class = SellOfferFiler

class RentOfferViewSet(ListAPIView):
    serializer_class = RentOfferSerializer
    filter_backends = (DjangoFilterBackend, )
    queryset = RentOffer.objects.all()
    filterset_class = RentOfferFiler
