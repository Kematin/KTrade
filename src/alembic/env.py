import asyncio
from logging.config import fileConfig

from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from config import get_config
from setup.base import Base

MODELS = ["models.table:Item"]

custom_config = get_config()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def register_models(base):
    for model_path in MODELS:
        module_path, class_name = model_path.split(":")
        module = __import__(module_path, fromlist=[class_name])
        model_class = getattr(module, class_name)


register_models(Base)

target_metadata = Base.metadata

db_url = (
    "postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
db_url = db_url.format(
    DB_USERNAME=custom_config.db.user,
    DB_PASSWORD=custom_config.db.password,
    DB_HOST=custom_config.db.host,
    DB_PORT=custom_config.db.port,
    DB_NAME=custom_config.db.name,
)
config.set_section_option(config.config_ini_section, "sqlalchemy.url", db_url)


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


run_migrations_online()
