"""Article schemas."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from src.schemas.tags_schema import Tags


class Article(BaseModel):
    """Base model for an article."""

    author: str = Field(example="Tobias Caliskan")
    tags: List[Tags] = Field(example=["React", "TailwindCSS", "NextJS"])
    image_url: str = Field(example="www.asset-monitoring.de/nice_picture.svg")
    title: str = Field(example="This is my awesome title")
    description: str = Field(
        min_length=40,
        max_length=140,
        example="This is my awesome description",
    )
    content: Optional[str] = Field(example="The content preferable in markdown")

    class Config:
        """Enable the ORM compatibility for SQLAlchemy."""

        orm_mode = True


class CreateArticle(Article):
    """Schema for creating a new article."""

    content: str = Field(example="My awesome title")


class ArticleCreated(Article):
    """Schema for a created article."""

    id: int
    content: str = Field(example="My new content in markdown")
    created_at: date


class UpdateArticle(Article):
    """Schema for updating an article.

    Inherits from the Article
    model and make all fields optional, since there is no partial
    option available in Pydantic :(
    """

    __annotations__ = {k: Optional[v] for k, v in Article.__annotations__.items()}


class ArticleUpdated(BaseModel):
    """Schema for a updated article."""

    article_id: int = Field(example=32)
    status: str = Field(example="Article updated")


class ArticleDeleted(BaseModel):
    """Schema for a deleted article."""

    article_id: int = Field(example=43)
    status: str = Field(example="Article deleted")


class ArticleDB(Article):
    """Schema for an article obtained from the database."""

    id: int
    created_at: date
    updated_at: Optional[date]
