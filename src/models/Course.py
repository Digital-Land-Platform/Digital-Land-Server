from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.CourseContent import CourseContent
from .Base import Base
import uuid

class Course(Base):
    __tablename__ = "courses"
    
    title = Column(String, nullable=False)
    description = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    contents = relationship("CourseContent", backref="course", cascade="all,delete, delete-orphan")
