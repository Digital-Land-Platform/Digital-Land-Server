import strawberry
from datetime import datetime
from src.models.enums.ContentType import ContentType
import strawberry
from typing import Optional
import uuid
from strawberry.file_uploads import Upload


@strawberry.input
class CourseContentCreateInput:
    content_type: ContentType
    content_url: Optional[str] = None  # Only used for VIDEO and REEL types
    text_content: Optional[str] = None  # Only used for ARTICLE and QUIZ types
    title: Optional[str] = None
    file: Optional[Upload] = None
@strawberry.input
class CourseContentUpdateInput:
    content_type: Optional[ContentType] = None
    content: Optional[str] = None
    title: Optional[str] = None
    file: Optional[Upload] = None
@strawberry.type
class CourseContentType:
    id: uuid.UUID
    content_type: ContentType
    content_url: Optional[str]
    text_content: Optional[str]
    title: Optional[str]
