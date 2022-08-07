from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from base.filters import RentOfferFilter, SellOfferFilter
from base.models import RentOffer, SellOffer
from base.serializers import RentOfferSerializer, SellOfferSerializer


class SellOfferView(ListAPIView):
    serializer_class = SellOfferSerializer
    filter_backends = (DjangoFilterBackend, )
    queryset = SellOffer.objects.all()
    filterset_class = SellOfferFilter
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'base/index.html'

    def get(self, request: HttpRequest):
        filtered = SellOfferFilter(request.GET).qs
        return Response({'sells': filtered})

class RentOfferView(ListAPIView):
    serializer_class = RentOfferSerializer
    filter_backends = (DjangoFilterBackend, )
    queryset = RentOffer.objects.all()
    filterset_class = RentOfferFilter
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'base/index.html'

    def get(self, request: HttpRequest):
        filtered = RentOfferFilter(request.GET).qs
        return Response({'sells': filtered})
