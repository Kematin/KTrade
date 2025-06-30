from typing import Optional

from pydantic import BaseModel, HttpUrl, model_validator

from models.table import Currency, GameType, Marketplace, Quality


class CSGOItemBase(BaseModel):
    name: str
    image_url: Optional[HttpUrl] = None
    price: float
    quality: Quality
    currency: Currency = Currency.USD
    float_value: float
    pattern: int


class CSGOItemResponse(CSGOItemBase):
    id: int

    class Config:
        from_attributes = True


class CustomItemBase(BaseModel):
    name: str
    image_url: str


class CustomItemCreate(CustomItemBase):
    pass


class CustomItemUpdate(BaseModel):
    name: Optional[str] = None
    image_path: Optional[str] = None


class CustomItemResponse(CustomItemBase):
    id: int

    class Config:
        from_attributes = True


class ItemOnSaleBase(BaseModel):
    quantity: int = 1
    game_type: GameType
    purchase_price: float
    selling_price: float
    source_marketplace: Marketplace
    target_marketplace: Marketplace
    currency: Currency = Currency.USD


class ItemOnSaleCreate(ItemOnSaleBase):
    csgo_item_id: Optional[int] = None
    custom_item_id: Optional[int] = None

    @model_validator(mode="after")
    def check_item_reference(cls, model):
        if model.custom_item_id == -1:
            return model
        if model.csgo_item_id is None and model.custom_item_id is None:
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
