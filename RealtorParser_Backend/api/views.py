from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import RentOffer, SellOffer
from api.serializers import RentOfferSerializer, SellOfferSerializer


@api_view(['GET'])
def sells(request: Request):
    items = SellOffer.objects.all()
    serialized = SellOfferSerializer(items, many=True)
    return Response(serialized.data)

@api_view(['GET'])
def rents(request: Request):
    items = RentOffer.objects.all()
    serialized = RentOfferSerializer(items, many=True)
    return Response(serialized.data)
