from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config import get_config
from routes import routes
from setup import configure_logger, create_test_data, init_db, teardown

config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logger()
    await init_db()
    if config.debug:
        logger.debug("Create test data")
        await create_test_data()
    yield
    await teardown()


app = FastAPI(lifespan=lifespan, title="Notes Backend")

for router in routes:
    app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("app:app", host=config.host, port=config.port, reload=config.debug)
