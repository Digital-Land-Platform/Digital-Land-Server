from sqlalchemy import Column, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from .enums.ContentType import ContentType
from .Base import Base
import uuid

class CourseContent(Base):
    __tablename__ = "course_contents"
    
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    content_type = Column(Enum(ContentType), nullable=False)
    title = Column(String, nullable=False)
    content_url = Column(String)
    text_content = Column(Text)
