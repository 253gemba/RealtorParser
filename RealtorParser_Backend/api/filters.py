from django_filters.rest_framework import (DateTimeFromToRangeFilter,
                                           FilterSet, RangeFilter)

from api.models import RentOffer, SellOffer


class SellOfferFiler(FilterSet):
    created = DateTimeFromToRangeFilter()
    area = RangeFilter()
    price = RangeFilter()
    floor = RangeFilter()
    floor_max = RangeFilter()

    class Meta():
        model = SellOffer
        fields = ['created', 'area', 'price', 'floor', 'floor_max']


class RentOfferFiler(FilterSet):
    created = DateTimeFromToRangeFilter()
    area = RangeFilter()
    floor = RangeFilter()
    floor_max = RangeFilter()

    class Meta():
        model = RentOffer
        fields = ['created', 'area', 'floor', 'floor', 'floor_max']
