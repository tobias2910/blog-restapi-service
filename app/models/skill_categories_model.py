from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)
