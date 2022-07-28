from dataclasses import dataclass


@dataclass(frozen=True)
class ItemInfo:
    card_link: str
    image_link: str
    name: str
    price: str
    location: str
    phone: str
