from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import CustomItem, ItemOnSale
from schemas import (
    CustomItemCreate,
    ItemOnSaleCreate,
    ItemOnSaleResponse,
    ItemOnSaleWithCustomItemCreate,
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
async def add_sale(
    item_data: ItemOnSaleCreate, session: AsyncSession = Depends(get_db)
):
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


@route.put("/sold/{item_id}", status_code=200)
async def change_status_sale(item_id: int, session: AsyncSession = Depends(get_db)):
    item = await session.get(ItemOnSale, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.is_sold = not item.is_sold

    await session.commit()
    return {"message": "Status updated"}


@route.delete("/{item_id}")
async def remove_sale(item_id: int, session: AsyncSession = Depends(get_db)):
    item = await session.get(ItemOnSale, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.delete(item)
    await session.commit()
    return {"message": "Item deleted"}


@route.post("/custom-with-sale", response_model=ItemOnSaleResponse)
async def add_custom_item_with_sale(
    combined_data: ItemOnSaleWithCustomItemCreate,
    session: AsyncSession = Depends(get_db),
):
    sale_data = combined_data.sale_data
    custom_item_data = combined_data.custom_item_data

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
