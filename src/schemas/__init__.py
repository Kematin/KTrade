from .base import CSGOItemBase, CustomItemBase
from .enums import Currency, GameId, GameType, Marketplace, Quality
from .items import (
    CSGOItemResponse,
    CustomItemCreate,
    CustomItemResponse,
    CustomItemUpdate,
    ItemOnSaleCreate,
    ItemOnSaleResponse,
    ItemOnSaleUpdate,
    ItemOnSaleWithCustomItemCreate,
)

pydantic_items = [
    CSGOItemResponse,
    CustomItemCreate,
    CustomItemResponse,
    CustomItemUpdate,
    ItemOnSaleUpdate,
    ItemOnSaleCreate,
    ItemOnSaleResponse,
    ItemOnSaleWithCustomItemCreate,
]

enums = [Currency, GameType, Marketplace, Quality, GameId]
base = [CSGOItemBase, CustomItemBase]

__all__ = enums + pydantic_items + base
