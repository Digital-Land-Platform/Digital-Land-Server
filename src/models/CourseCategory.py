from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .Base import Base

class CourseCategory(Base):
    __tablename__ = "course_categories"

    
    name = Column(String, nullable=False, unique=True)  # Name of the category
