from django.urls import path
from .views import sells, rents

urlpatterns = [
    path('sells/', sells),
    path('rents/', rents)
]