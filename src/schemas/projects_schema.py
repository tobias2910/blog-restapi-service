"""Projects schemas."""
from typing import List, Optional

from pydantic import BaseModel, Field

from src.schemas.tags_schema import Tags


class Project(BaseModel):
    """Base model for a project."""

    title: str = Field(example="This is my awesome title")
    image_url: str = Field(example="www.asset-monitoring.de/nice_picture.svg")
    description: str = Field(
        min_length=40,
        max_length=140,
        example="This is my awesome description",
    )
    project_url: str = Field(example="www.asset-monitoring.de")
    tags: List[Tags] = Field(example=["React", "TailwindCSS", "NextJS"])

    class Config:
        """Enable the ORM compatibility for SQLAlchemy."""

        orm_mode = True


class ProjectCreated(Project):
    """Schema for a created project."""

    id: int


class UpdateProject(Project):
    """Schema for updating an project.

    Inherits from the Project model and make all fields optional,
    since there is no partial option available in Pydantic :(.
    """

    __annotations__ = {k: Optional[v] for k, v in Project.__annotations__.items()}


class ProjectUpdated(BaseModel):
    """Schema for a updated project."""

    project_id: int = Field(example=32)
    status: str = Field(example="Project updated")


class ProjectDeleted(BaseModel):
    """Schema for a deleted project."""

    project_id: int = Field(example=43)
    status: str = Field(example="Project deleted")


class ProjectDB(Project):
    """Schema representing the project obtained from the database."""

    id: int
