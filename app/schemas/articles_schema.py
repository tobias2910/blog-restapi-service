from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Article(BaseModel):
    """
    Base model for an article
    """

    author: str
    tags: Union[List[str], str]
    image_url: str
    title: str
    description: str = Field(min_length=40, max_length=140)
    content: str

    class Config:
        orm_mode = True


class ArticleCreated(Article):
    """
    Response for an created article
    """

    id: int
    tags: str
    created_at: datetime


class ArticleUpdate(Article):
    """
    Model for updating an article. Inherits from the Article
    model and make all fields optional, since there is no partial
    option available in Pydantic :(
    """

    __annotations__ = {k: Optional[v] for k, v in Article.__annotations__.items()}
