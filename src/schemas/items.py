from typing import Optional

from pydantic import BaseModel, model_validator

from .base import CSGOItemBase, CustomItemBase, ItemOnSaleBase
from .enums import Currency, Marketplace


class CSGOItemResponse(CSGOItemBase):
    id: int

    class Config:
        from_attributes = True


class CustomItemCreate(CustomItemBase):
    pass


class CustomItemUpdate(BaseModel):
    name: Optional[str] = None
    image_path: Optional[str] = None


class CustomItemResponse(CustomItemBase):
    id: int

    class Config:
        from_attributes = True


class ItemOnSaleCreate(ItemOnSaleBase):
    csgo_item_id: Optional[int] = None
    custom_item_id: Optional[int] = None

    @model_validator(mode="after")
    def check_item_reference(cls, model):
        if model.custom_item_id <= 0:
            model.custom_item_id = None
        if model.csgo_item_id <= 0:
            model.csgo_item_id = None

        if not model.csgo_item_id and not model.custom_item_id:
            raise ValueError("Either csgo_item_id or custom_item_id must be provided")
        if model.csgo_item_id and model.custom_item_id:
            raise ValueError("Only one type of item id can be provided")
        return model


class ItemOnSaleUpdate(BaseModel):
    quantity: Optional[int] = None
    purchase_price: Optional[float] = None
    selling_price: Optional[float] = None
    source_marketplace: Optional[Marketplace] = None
    target_marketplace: Optional[Marketplace] = None
    currency: Optional[Currency] = None


class ItemOnSaleResponse(ItemOnSaleBase):
    id: int
    csgo_item: Optional[CSGOItemResponse] = None
    custom_item: Optional[CustomItemResponse] = None

    class Config:
        from_attributes = True


class ItemOnSaleWithCustomItemCreate(BaseModel):
    sale_data: ItemOnSaleBase
    custom_item_data: CustomItemCreate
