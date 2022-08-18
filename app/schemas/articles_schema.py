from datetime import date
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Article(BaseModel):
    """
    Base model for an article
    """

    author: str = Field(example="Tobias Caliskan")
    tags: Union[List[str], str] = Field(example=["React", "TailwindCSS", "NextJS"])
    image_url: str = Field(example="www.asset-monitoring.de/nice_picture.svg")
    title: str = Field(example="This is my awesome title")
    description: str = Field(
        min_length=40,
        max_length=140,
        example="This is my awesome description",
    )
    content: Optional[str] = Field(example="This is my content preferable in markdown.")

    class Config:
        orm_mode = True


class CreateArticle(Article):
    """
    Schema for creating a new article
    """

    tags: List[str] = Field(example=["React", "TailwindCSS", "NextJS"])
    content: str = Field(example="My awesome title")


class ArticleCreated(Article):
    """
    Schema for a created article
    """

    id: int
    tags: str = Field(example=["React", "TailwindCSS", "NextJS"])
    content: str = Field(example="My new content in markdown")
    created_at: date


class UpdateArticle(Article):
    """
    Schema for updating an article. Inherits from the Article
    model and make all fields optional, since there is no partial
    option available in Pydantic :(
    """

    __annotations__ = {k: Optional[v] for k, v in Article.__annotations__.items()}


class ArticleUpdated(BaseModel):
    """
    Schema for a updated article
    """

    article_Id: int = Field(example=32)
    status: str = Field(example="Article updated")


class ArticleDeleted(BaseModel):
    """
    Schema for a deleted article
    """

    article_Id: int = Field(example=43)
    status: str = Field(example="Article deleted")


class ArticleDB(Article):
    """
    Schema representing the article obtained from the database
    """

    id: int
    created_at: date
    updated_at: Optional[date]
