from sqlalchemy import Column, String, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.CourseContent import CourseContent
from src.models.enums.CourseCategory import CourseCategory
from src.models.CourseCategory import CourseCategory
from src.models.enums.ContentStatus import ContentStatus
from .Base import Base
import uuid
import enum

class Course(Base):
    __tablename__ = "courses"
    
    title = Column(String, nullable=False)
    description = Column(Text)
    category_id = Column(UUID(as_uuid=True), ForeignKey("course_categories.id"), nullable=False)
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT)
    target_audience = Column(String)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    contents = relationship("CourseContent", backref="course", cascade="all,delete, delete-orphan")
    category = relationship("CourseCategory", backref="courses")
