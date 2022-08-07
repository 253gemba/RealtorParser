from rest_framework import serializers

from base.models import RentOffer, SellOffer


class SellOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellOffer
        fields = '__all__'


class RentOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentOffer
        fields = '__all__'
