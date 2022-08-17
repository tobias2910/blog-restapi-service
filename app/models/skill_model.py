from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
    name = Column(String, index=True)
    skill_level_id = Column(Integer, ForeignKey("skill_levels.id"))
    skill_level = relationship("SkillLevel")
