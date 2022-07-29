from dataclasses import dataclass


@dataclass(frozen=True)
class SellOffer:
    card_link: str
    image_link: str | None
    name: str
    description: str | None
    price: int
    location: str
    metro: str | None
    phone: str | None
    area: float
    floor: int
    floor_max: int
