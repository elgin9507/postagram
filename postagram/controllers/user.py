"""User controller module."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from postagram import settings
from postagram.db.database import get_db
from postagram.domain import auth
from postagram.domain.user import create_new_user
from postagram.schemas import user as schemas

router = APIRouter()


@router.post("/login/")
async def login(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db),
) -> schemas.Token:
    """Authenticate a user and return an access token."""

    user = auth.authenticate_user(credentials.email, credentials.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION)
    access_token = auth.create_access_token(
        data=schemas.TokenData(username=user.email).dict(),
        expires_delta=access_token_expires,
    )

    return schemas.Token(access_token=access_token)


@router.post("/signup/")
async def signup(
    credentials: schemas.UserSignUp,
    db: Session = Depends(get_db),
):
    """Create a new user and return an access token."""

    user = auth.get_user(credentials.email, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = create_new_user(
        credentials.email, auth.get_password_hash(credentials.password), db
    )
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION)
    access_token = auth.create_access_token(
        data=schemas.TokenData(username=new_user.email).dict(),
        expires_delta=access_token_expires,
    )

    return schemas.Token(access_token=access_token)
