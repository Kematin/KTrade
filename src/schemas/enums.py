from enum import Enum as PyEnum


class GameType(PyEnum):
    DOTA = "Dota 2"
    CS2 = "Counter-Strike 2"  # ! Delete
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


class GameId(PyEnum):
    CSGO = 730
    DOTA2 = 570
