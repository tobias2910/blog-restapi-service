from src.db.base import Base
from sqlalchemy import Column, Integer, String


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    image_url = Column(String)
    description = Column(String)
    project_url = Column(String)
    tags = Column(String)
