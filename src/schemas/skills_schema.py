"""Skills schemas."""
from typing import Optional

from pydantic import BaseModel, Field


class SkillSchema(BaseModel):
    """The base model for managing skills."""

    name: str = Field(example="TailwindCSS", description="The name of the skill.")
    category: str = Field(example="Languages", description="The category of the skill.")
    experience: int = Field(example=2, ge=1, le=3, description="The level of experience for the skill.")


class SkillDB(SkillSchema):
    """The model representing the result from the DB."""

    id: int

    class Config:
        """Enable the ORM compatibility for SQLAlchemy."""

        orm_mode = True


class UpdateSkill(SkillSchema):
    """Schema for updating an skill.

    Inherits from the Skill model and make all fields optional,
    since there is no partial option available in Pydantic :(.
    """

    __annotations__ = {k: Optional[v] for k, v in SkillSchema.__annotations__.items()}


class SkillAdjusted(BaseModel):
    """The model for deleting a user."""

    skill_id: int
    status: str = Field(example="User successfully deleted")
