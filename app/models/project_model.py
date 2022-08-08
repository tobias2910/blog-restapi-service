from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    imageUrl = Column(String)
    description = Column(String)
    project_url = Column(String)
    tags = Column(String)
