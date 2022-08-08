from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import DATE

from app.db.base import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String, index=True)
    image_url = Column(String)
    description = Column(String)
    content = Column(String)
    tags = Column(String)
    created_at = Column(DATE, nullable=False)
    updated_at = Column(DATE)
