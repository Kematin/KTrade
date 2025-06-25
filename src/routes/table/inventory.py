from fastapi import APIRouter, status

route = APIRouter(prefix="/inventory", tags=["Inventory"])


@route.get("/")
async def get_inventory(skip: int = 0, limit: int = 50):
    return {"yo": "yo"}
