"""Skills schemas."""
from typing import Optional

from pydantic import BaseModel, Field


class SkillSchema(BaseModel):
    """The base model for managing skills."""

    name: str = Field(example="TailwindCSS")
    experience: int = Field(example=2, ge=1, le=3)


class SkillDB(SkillSchema):
    """The model representing the result from the DB."""

    id: int


class UpdateSkill(SkillSchema):
    """Schema for updating an skill.

    Inherits from the Skill model and make all fields optional,
    since there is no partial option available in Pydantic :(.
    """

    __annotations__ = {k: Optional[v] for k, v in SkillSchema.__annotations__.items()}


class SkillAdjusted(SkillDB):
    """The model for deleting a user."""

    status: str = Field(example="User successfully deleted")
