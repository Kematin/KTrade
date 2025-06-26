from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import get_config

config = get_config()

db_url = (
    "postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(
    db_url.format(
        DB_USERNAME=config.db.user,
        DB_PASSWORD=config.db.password,
        DB_HOST=config.db.host,
        DB_PORT=config.db.port,
        DB_NAME=config.db.name,
    ),
    echo=False,
)

sessionmaker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSession() as session:
        yield session


async def init_db():
    async with engine.begin() as _:
        ...
        # await conn.run_sync(Base.metadata.create_all)


async def teardown():
    await engine.dispose()


async def create_test_data():
    from sqlalchemy import insert

    from models.table import CSGOItem, Currency, Quality

    items_data = [
        {
            "name": "AK-47 | Redline",
            "image_url": "https://steamcommunity.com/image/ak47_redline.jpg",
            "price": 45.99,
            "quality": Quality.MW,
            "currency": Currency.USD,
            "float_value": 0.12345678,
            "pattern": 123,
        },
    ]

    async with sessionmaker() as session:
        await session.execute(insert(CSGOItem), items_data)
        await session.commit()
