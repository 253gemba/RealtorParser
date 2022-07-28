from dataclasses import dataclass


@dataclass(frozen=True)
class ItemInfo:
    card_link: str
    image_link: str | None
    name: str
    description: str | None
    price: str
    location: str
    metro: str | None
    phone: str | None
    area: float
    floor: int
    floor_max: int
