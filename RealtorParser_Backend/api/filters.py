from django_filters.rest_framework import (DateTimeFromToRangeFilter,
                                           FilterSet, RangeFilter)

from api.models import RentOffer, SellOffer


class OfferFilter(FilterSet):
    created = DateTimeFromToRangeFilter()
    area = RangeFilter()
    price = RangeFilter()
    floor = RangeFilter()
    floor_max = RangeFilter() 


class SellOfferFilter(OfferFilter):
    class Meta():
        model = SellOffer
        fields = ['created', 'area', 'price', 'floor', 'floor_max']


class RentOfferFilter(OfferFilter):
    class Meta():
        model = RentOffer
        fields = ['created', 'area', 'price', 'floor', 'floor_max']
