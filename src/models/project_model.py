"""Project model for the database."""
from sqlalchemy import Column, Integer, String

from src.db.base import Base


class Project(Base):
    """Represents the projects table in the database."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    image_url = Column(String)
    description = Column(String)
    project_url = Column(String)
    tags = Column(String)
