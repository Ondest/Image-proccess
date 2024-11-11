from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.kafka.kafka_client import kafka_client

from .endpoints.images import router as image_router
from .endpoints.auth import router as auth_router

from pathlib import Path


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    pool = aioredis.ConnectionPool.from_url(url=settings.redis_url)
    redis_ = aioredis.Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(redis_), prefix="cache:")

    await kafka_client.start()

    yield

    await kafka_client.stop()


app = FastAPI(title="Image API", lifespan=lifespan)

static_folder_path = Path(__file__).parent
app.mount("/static", StaticFiles(directory=static_folder_path), name="static")

app.include_router(image_router, prefix="/images", tags=["images"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Authorization",
    ],
)
