from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import CustomItem
from schemas import (
    CustomItemCreate,
    CustomItemResponse,
)
from utils.database import get_db

route = APIRouter(prefix="/inventory", tags=["Inventory"])


@route.get("/")
async def get_inventory(skip: int = 0, limit: int = 50):
    return {"yo": "yo"}


@route.post("/custom", response_model=CustomItemResponse)
async def add_custom_item(
    item_data: CustomItemCreate, session: AsyncSession = Depends(get_db)
):
    db_item = CustomItem(**item_data.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


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
