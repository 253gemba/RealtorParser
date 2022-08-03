from django.urls import path

from .views import RentOfferViewSet, SellOfferViewSet

urlpatterns = [
    path('sells/', SellOfferViewSet.as_view()),
    path('rents/', RentOfferViewSet.as_view())
]