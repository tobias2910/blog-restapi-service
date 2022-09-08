"""User model for the database."""
from sqlalchemy import Column, ForeignKey, Integer, String

from src.db.base import Base


class Skill(Base):
    """Represents the categories table in the database."""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, index=True)
    skill_level_id = Column(Integer, ForeignKey("skill_levels.id"))
