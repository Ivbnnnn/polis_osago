from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.logger import logger, setup_logging
from app.api.fake_data import router as fake_router
from app.api.search import router as search_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    setup_logging()
    logger.info("Info API running")
    yield
    logger.info("Info API closed")



app=FastAPI(lifespan=lifespan)

app.include_router(fake_router)
app.include_router(search_router)