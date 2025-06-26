from typing import List

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import ItemOnSale
from pydantic_models import ItemOnSaleCreate, ItemOnSaleResponse
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


"""


@route.delete("/{item_id}")
async def remove_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(ItemOnSale, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)
    await db.commit()
    return {"message": "Item deleted"}


@route.post("/custom", response_model=CustomItemResponse)
async def add_custom_item(
    item_data: CustomItemCreate, db: AsyncSession = Depends(get_db)
):
    db_item = CustomItem(**item_data.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@route.put("/custom/{item_id}", response_model=CustomItemResponse)
async def change_custom_item(
    item_id: int, item_data: CustomItemCreate, db: AsyncSession = Depends(get_db)
):
    item = await db.get(CustomItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in item_data.dict().items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@route.delete("/custom/{item_id}")
async def remove_custom_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(CustomItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)
    await db.commit()
    return {"message": "Custom item deleted"}

"""
