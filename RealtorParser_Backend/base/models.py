from django.db.models import (CharField, DateTimeField, FloatField,
                              IntegerField, Model, TextField, URLField)


class Offer(Model):
    card_link = URLField(max_length=500)
    image_link = URLField(max_length=500, blank=True, null=True)
    name = CharField(max_length=500)
    description = TextField(blank=True, null=True)
    price = IntegerField()
    location = CharField(max_length=500)
    metro = CharField(max_length=500, blank=True, null=True)
    phone = CharField(max_length=200, blank=True, null=True)
    area = FloatField()
    floor = IntegerField()
    floor_max = IntegerField()
    created = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class SellOffer(Offer):
    pass


class RentOffer(Offer):
    price_day = 'day'
    price_month = 'month'
    price_per = CharField(max_length=200, choices=((price_day, 'день'), (price_month, 'месяц')))
