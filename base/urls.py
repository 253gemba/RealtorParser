from django.urls import path

from .views import RentOfferView, SellOfferView

urlpatterns = [
    path('sells/', SellOfferView.as_view()),
    path('rents/', RentOfferView.as_view())
]