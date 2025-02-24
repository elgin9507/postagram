"""User module related services."""

import uuid
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from postagram import settings
from postagram.db.database import get_db
from postagram.models.user import User
from postagram.schemas import user as schemas


def create_new_user(email: str, hashed_password: str, db: Session) -> User:
    """User factory function."""

    new_user = User(
        id=str(uuid.uuid4()),
        email=email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(username: str, db: Session) -> User:
    """Retrieve a user by its username."""

    return db.query(User).filter(User.email == username).first()


async def get_current_user(
    token: Annotated[str, Header()], db: Session = Depends(get_db)
):
    """Retrieve the current user from the request token.

    This function is a dependency for FastAPI and should be used when
    a route requires authentication.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user
