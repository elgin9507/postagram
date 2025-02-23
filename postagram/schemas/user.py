"""Schemas for user related operations."""

from pydantic import BaseModel, EmailStr, Field


class _UserAuth(BaseModel):
    """Base schema for user authentication."""

    email: EmailStr = Field(..., description="The email address of the user.")
    password: str = Field(..., description="The password of the user.")

    class Config:
        json_schema_extra = {
            "example": {"email": "user@mail.com", "password": "password"}
        }


class UserSignUp(_UserAuth):
    """Schema for user sign up."""

    pass


class UserLogin(_UserAuth):
    """Schema for user login."""

    pass


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(..., description="The JWT access token.")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIifQ.eyJleHAiOjE2MzIwNzUwNzYsImlhdCI6MTYzMjA3NDQ3Niwic3ViIjoxfQ.7J1"
            }
        }


class TokenData(BaseModel):
    """Schema for JWT token data."""

    username: str | None = None
