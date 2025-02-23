"""In-memory caching services."""

from fastapi_cache import FastAPICache

from postagram import settings
from postagram.models.user import User


def post_generate_cache_key(user: User) -> str:
    """Generate a cache key for a user's posts."""

    return f"{settings.POST_CACHE_NAMESPACE}:{user.id}"


async def post_invalidate_cache(user: User) -> None:
    """Invalidate a user's post cache."""

    cache_backend = FastAPICache.get_backend()
    await cache_backend.clear(namespace=settings.POST_CACHE_NAMESPACE, key=user.id)


def post_cache_key_builder(func, namespace: str = "", **kwargs):
    """Build a cache key for a user's posts.

    Callback function for the `fastapi_cache.decorator.cache` decorator.
    """

    args = kwargs.get("args", ())
    user = args[0] if args else None  # Extract `user` from `args`

    if not user or not isinstance(user, User):
        return "posts:anonymous"  # Default key to prevent caching errors

    return post_generate_cache_key(user)
