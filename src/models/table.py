from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import relationship

from setup.base import Base


class GameType(PyEnum):
    DOTA = "Dota 2"
    CS2 = "Counter-Strike 2"
    TF2 = "Team Fortress 2"
    RUST = "Rust"
    CSGO = "CSGO"


class Marketplace(PyEnum):
    STEAM = "Steam"
    TM = "TMarket"
    CSMONEY = "CSMoney"
    LOOTFARM = "LootFarm"
    TRADEIT = "TradeIT"


class Quality(PyEnum):
    BS = "BS"
    WW = "WW"
    FT = "FT"
    MW = "MW"
    FN = "FN"


class Currency(PyEnum):
    USD = "USD"
    RUB = "RUB"


class CustomItem(Base):
    __tablename__ = "custom_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    image_url = Column(String(255))

    sales = relationship(
        "ItemOnSale",
        back_populates="custom_item",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<CustomItem(id={self.id}, name={self.name})>"


class CSGOItem(Base):
    __tablename__ = "csgo_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    image_url = Column(String(255))
    price = Column(NUMERIC(12, 2))
    quality = Column(Enum(Quality), nullable=False)
    currency = Column(Enum(Currency), default=Currency.USD)
    float_value = Column(NUMERIC(18, 16))
    pattern = Column(Integer)
    is_void = Column(Boolean, default=False)

    sales = relationship(
        "ItemOnSale",
        back_populates="csgo_item",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<CSGOItem(id={self.id}, name={self.name}, price={self.price} {self.currency})>"


class ItemOnSale(Base):
    __tablename__ = "items_on_sale"

    id = Column(Integer, primary_key=True, autoincrement=True)
    csgo_item_id = Column(Integer, ForeignKey("csgo_items.id"), nullable=True)
    custom_item_id = Column(Integer, ForeignKey("custom_items.id"), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    game_type = Column(Enum(GameType), nullable=False)
    purchase_price = Column(NUMERIC(12, 2), nullable=False)
    selling_price = Column(NUMERIC(12, 2), nullable=False)
    source_marketplace = Column(Enum(Marketplace), nullable=False)
    target_marketplace = Column(Enum(Marketplace), nullable=False)
    currency = Column(Enum(Currency), default=Currency.USD)
    is_sold = Column(Boolean, default=False)

    csgo_item = relationship(
        "CSGOItem",
        back_populates="sales",
    )

    custom_item = relationship(
        "CustomItem",
        back_populates="sales",
    )

    @property
    def item(self):
        return self.csgo_item if self.game_type == "CSGO" else self.custom_item

    def __repr__(self):
        return f"<ItemOnSale(id={self.id}, item_id={self.item_id}, quantity={self.quantity})>"
