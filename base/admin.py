from django.contrib import admin

from .models import RentOffer, SellOffer

admin.site.register(SellOffer)
admin.site.register(RentOffer)
