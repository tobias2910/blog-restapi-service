"""Tags schemas."""
from pydantic import BaseModel


class Tags(BaseModel):
    """Base schema for the Tags model."""

    icon_name: str
    name: str
