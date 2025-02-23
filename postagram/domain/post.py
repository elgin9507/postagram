"""Post module related services."""

import uuid

from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from postagram import settings
from postagram.domain.cache import post_cache_key_builder, post_invalidate_cache
from postagram.models.post import Post
from postagram.models.user import User


@cache(expire=settings.POST_CACHE_EXPIRATION, key_builder=post_cache_key_builder)
async def get_posts_for_user(user: User) -> list[Post]:
    return user.posts


def get_post_by_id(post_id: str, db: Session) -> Post:
    return db.query(Post).filter(Post.id == post_id).first()


def get_post_for_user(user: User, post_id: str, db: Session) -> Post:
    post = get_post_by_id(post_id, db)
    if post is not None and post.user_id == user.id:
        return post


async def delete_post_for_user(user: User, post: Post, db: Session) -> None:
    if post.user_id != user.id:
        raise ValueError("User does not own post")

    db.delete(post)
    db.commit()
    await post_invalidate_cache(user)


async def create_post_for_user(user: User, text: str, db: Session) -> Post:
    new_post = Post(id=str(uuid.uuid4()), user_id=user.id, text=text)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    await post_invalidate_cache(user)

    return new_post
