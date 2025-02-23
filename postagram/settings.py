"""Settings for the Postagram application."""

import os

SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASE_URL = os.environ.get("DATABASE_URL")

JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
_30_minutes = 30 * 60
JWT_EXPIRATION = int(os.environ.get("JWT_EXPIRATION", _30_minutes))


REDIS_URL = os.environ.get("REDIS_URL")
_5_minutes = 5 * 60
POST_CACHE_NAMESPACE = os.environ.get("POST_CACHE_NAMESPACE", "posts")
POST_CACHE_EXPIRATION = int(os.environ.get("POST_CACHE_EXPIRATION", _5_minutes))
