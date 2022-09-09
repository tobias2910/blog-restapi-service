"""User model for the database."""
from sqlalchemy import Column, Integer, String

from src.db.base import Base


class Skill(Base):
    """Represents the categories table in the database."""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    experience = Column(Integer)
