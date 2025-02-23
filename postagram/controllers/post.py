"""Post controller module."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from postagram.db.database import get_db
from postagram.domain.post import (
    create_post_for_user,
    delete_post_for_user,
    get_post_for_user,
    get_posts_for_user,
)
from postagram.domain.user import get_current_user
from postagram.models.user import User
from postagram.schemas.post import PostCreateRequest, PostCreateResponse, PostDetail

router = APIRouter()


@router.get("/")
async def get_posts(
    user: Annotated[User, Depends(get_current_user)],
) -> list[PostDetail]:
    """List all posts for the current user."""

    posts = await get_posts_for_user(user)

    return posts


@router.post("/")
async def create_post(
    post_data: PostCreateRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> PostCreateResponse:
    """Create a new post for the current user."""

    new_post = await create_post_for_user(user, post_data.text, db)

    return PostCreateResponse(id=new_post.id)


@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> Response:
    """Delete a post for the current user."""

    post = get_post_for_user(user, post_id, db)

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    await delete_post_for_user(user, post, db)

    return Response(status_code=204)
