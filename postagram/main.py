"""Main module for the Postagram API."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from postagram import settings
from postagram.controllers.post import router as post_router
from postagram.controllers.user import router as user_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Postagram API",
    description="API for CRUD operations on posts",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(post_router, prefix="/posts", tags=["posts"])
