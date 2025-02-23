"""Authentication services."""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from postagram import settings
from postagram.domain.user import get_user
from postagram.models import user as models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """Verifies the plain password against the hashed password."""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Generates a hashed password from the plain password."""

    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session) -> models.User | bool:
    """Authenticates a user by verifying the username and password against the database."""
    user = get_user(username, db)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Generates an access token from the given data."""

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt
