from typing import List

from pydantic import BaseModel, Field


class Article(BaseModel):
    """
    Base model for an article
    """

    author: str
    tags: List[str]
    imageUrl: str
    title: str
    summary: str = Field(min_length=40, max_length=140)
    content: str


class ArticleCreated(Article):
    """
    Response for an created article
    """

    created: str


class ArticleUpdated(ArticleCreated):
    """
    Response for an updated article
    """

    updated: str
