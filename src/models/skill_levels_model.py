from src.db.base import Base
from sqlalchemy import Column, Integer, String


class SkillLevel(Base):
    __tablename__ = "skill_levels"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
