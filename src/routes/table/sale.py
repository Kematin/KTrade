from typing import List

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import CustomItem, ItemOnSale
from schemas import (
    CustomItemCreate,
    CustomItemResponse,
    ItemOnSaleCreate,
    ItemOnSaleResponse,
)
from utils.database import get_db

route = APIRouter(prefix="/sale", tags=["Sale"])


@route.get("/", response_model=List[ItemOnSaleResponse])
async def get_sale(
    skip: int = 0,
    limit: int = 50,
    is_sold: bool = False,
    session: AsyncSession = Depends(get_db),
):
    query = (
        select(ItemOnSale)
        .options(
            selectinload(ItemOnSale.csgo_item), selectinload(ItemOnSale.custom_item)
        )
        .offset(skip)
        .limit(limit)
        .where(ItemOnSale.is_sold == is_sold)
    )

    result = await session.execute(query)
    items = result.scalars().all()

    return items


@route.post("/", response_model=ItemOnSaleResponse)
async def add_item(
    item_data: ItemOnSaleCreate, session: AsyncSession = Depends(get_db)
):
    if item_data.game_type == "csgo" and not item_data.csgo_item_id:
        raise HTTPException(status_code=400, detail="CSGO item ID required")
    if item_data.game_type == "custom" and not item_data.custom_item_id:
        raise HTTPException(status_code=400, detail="Custom item ID required")

    db_item = ItemOnSale(**item_data.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    query = select(ItemOnSale).where(ItemOnSale.id == db_item.id)

    if db_item.csgo_item_id:
        query = query.options(selectinload(ItemOnSale.csgo_item))
    if db_item.custom_item_id:
        query = query.options(selectinload(ItemOnSale.custom_item))

    result = await session.execute(query)
    full_item = result.scalar_one()

    return full_item


@route.post("/sold/{item_id}", status_code=200)
async def change_status_item(item_id: int, session: AsyncSession = Depends(get_db)):
    item = await session.get(ItemOnSale, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.is_sold = not item.is_sold

    await session.commit()
    return {"message": "Status updated"}


@route.delete("/{item_id}")
async def remove_item(item_id: int, session: AsyncSession = Depends(get_db)):
    item = await session.get(ItemOnSale, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.delete(item)
    await session.commit()
    return {"message": "Item deleted"}


@route.post("/custom", response_model=CustomItemResponse)
async def add_custom_item(
    item_data: CustomItemCreate, session: AsyncSession = Depends(get_db)
):
    db_item = CustomItem(**item_data.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@route.post("/custom-with-sale", response_model=ItemOnSaleResponse)
async def add_custom_item_with_sale(
    custom_item_data: CustomItemCreate,
    sale_data: ItemOnSaleCreate,
    session: AsyncSession = Depends(get_db),
):
    if not sale_data.custom_item_id:
        db_custom_item = CustomItem(**custom_item_data.model_dump())
        session.add(db_custom_item)
        await session.flush()

    sale_data_dict = sale_data.model_dump()
    sale_data_dict.update({"custom_item_id": db_custom_item.id})

    db_sale_item = ItemOnSale(**sale_data_dict)
    session.add(db_sale_item)
    await session.commit()

    result = await session.execute(
        select(ItemOnSale)
        .options(selectinload(ItemOnSale.custom_item))
        .where(ItemOnSale.id == db_sale_item.id)
    )

    return result.scalar_one()


@route.put("/custom/{item_id}", response_model=CustomItemResponse)
async def change_custom_item(
    item_id: int, item_data: CustomItemCreate, session: AsyncSession = Depends(get_db)
):
    item = await session.get(CustomItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in item_data.model_dump().items():
        setattr(item, field, value)

    await session.commit()
    await session.refresh(item)
    return item


@route.delete("/custom/{item_id}")
async def remove_custom_item(item_id: int, session: AsyncSession = Depends(get_db)):
    item = await session.get(CustomItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.delete(item)
    await session.commit()
    return {"message": "Custom item deleted"}
