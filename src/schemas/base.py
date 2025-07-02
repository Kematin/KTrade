from typing import Optional

from pydantic import BaseModel, HttpUrl

from .enums import Currency, Quality


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
