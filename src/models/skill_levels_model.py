"""User model for the database."""
from sqlalchemy import Column, Integer, String

from src.db.base import Base


class SkillLevel(Base):
    """Represents the article table in the database."""

    __tablename__ = "skill_levels"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
