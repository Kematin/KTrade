from typing import Optional

from pydantic import BaseModel, HttpUrl

from .enums import Currency, GameType, Marketplace, Quality


class CSGOItemBase(BaseModel):
    name: str
    image_url: Optional[HttpUrl] = None
    price: float
    quality: Quality
    currency: Currency = Currency.USD
    float_value: float
    pattern: int


class CustomItemBase(BaseModel):
    name: str
    image_url: str
    price: float
    currency: Currency = Currency.USD
    game_type: GameType


class ItemOnSaleBase(BaseModel):
    quantity: int = 1
    purchase_price: float
    selling_price: float
    commission: int
    source_marketplace: Marketplace
    target_marketplace: Marketplace
    currency: Currency = Currency.USD
