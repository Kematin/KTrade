from typing import List, Union

from config import get_config
from schemas import CSGOItemBase, CustomItemBase, GameId
from serivces.parser import fetch_data

config = get_config()
STEAM_ID = config.steam.client_id
BASE_URL = (
    "https://steamcommunity.com/inventory/{steam_id}/{game_id}/2?l=russian&count=1000"
)


async def fetch_steam_inventory() -> List[Union[CSGOItemBase, CustomItemBase]]:
    csgo_items = await fetch_csgo_items()
    dota_items = []
    # dota_items = await fetch_dota_items()
    return csgo_items + dota_items


async def fetch_csgo_items() -> List[CSGOItemBase]:
    url = BASE_URL.format(steam_id=STEAM_ID, game_id=GameId.CSGO)
    dataInventory = await fetch_data(url)


async def fetch_dota_items() -> List[CustomItemBase]:
    url = BASE_URL.format(steam_id=STEAM_ID, game_id=GameId.DOTA2)
    dataInventory = await fetch_data(url)
