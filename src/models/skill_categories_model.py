"""User model for the database."""
from sqlalchemy import Column, Integer, String

from src.db.base import Base


class Category(Base):
    """Represents the categories table in the database."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)
