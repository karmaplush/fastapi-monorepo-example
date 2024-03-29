from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from routers import root, threads, users


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("👋✨ Hello from started Api service.")

    app.include_router(root.router)
    app.include_router(users.router)
    app.include_router(threads.router)

    yield

    logger.info("👋😢 Goodbye from stopped Api service")


app = FastAPI(lifespan=lifespan)
