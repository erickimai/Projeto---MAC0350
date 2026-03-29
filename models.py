from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # One Category -> Many Tasks
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Many Tasks -> One Category
    category = relationship("Category", back_populates="tasks")
