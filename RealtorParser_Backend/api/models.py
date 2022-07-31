from django.db import models


class SellOffer(models.Model):
    card_link = models.URLField(max_length=500)
    image_link = models.URLField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    location = models.CharField(max_length=500)
    metro = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    area = models.FloatField()
    floor = models.IntegerField()
    floor_max = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class RentOffer(models.Model):
    card_link = models.URLField(max_length=500)
    image_link = models.URLField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=200)
    location = models.CharField(max_length=500)
    metro = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    area = models.FloatField()
    floor = models.IntegerField()
    floor_max = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
