"""Schemas for post related operations."""

from pydantic import BaseModel, Field, field_validator


class _PostId(BaseModel):
    """Base schema for post ID."""

    id: str = Field(..., description="The unique identifier of the post.")


class _PostText(BaseModel):
    """Base schema for post text."""

    text: str = Field(..., description="The content of the post.")


class PostCreateRequest(_PostText):
    """Schema for creating a post."""

    @field_validator("text")
    @classmethod
    def check_byte_size(cls, value: str) -> str:
        """Check if the text is less than 1MB in size."""

        if len(value.encode("utf-8")) > 1_048_576:  # 1MB in bytes
            raise ValueError("Text exceeds 1MB in size")

        return value


class PostCreateResponse(_PostId):
    """Schema for the response of creating a post."""

    class Config:
        orm_mode = True
        json_schema_extra = {"example": {"id": "d290f1ee-6c54-4b01-90e6-d701748f0851"}}


class PostDetail(_PostId, _PostText):
    """Schema for the details of a post."""

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "text": "Hello, World!",
            }
        }


class PostDelete(_PostId):
    """Schema for deleting a post."""

    class Config:
        orm_mode = True
        json_schema_extra = {"example": {"id": "d290f1ee-6c54-4b01-90e6-d701748f0851"}}
