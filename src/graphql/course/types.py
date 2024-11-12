import strawberry
import uuid
from typing import List, Optional
from src.models.enums.ContentStatus import ContentStatus
from src.models.enums.CourseCategory import CourseCategory




@strawberry.input
class CourseCreateInput:
    title: str
    description: str
    #category: CourseCategory
    category_id: uuid.UUID
    status: ContentStatus
    
@strawberry.input
class CourseUpdateInput:
    title: Optional[str] = None
    description: Optional[str] = None
    #category: Optional[CourseCategory] = None
    category_id: Optional[uuid.UUID] = None
    status: Optional[ContentStatus] = None

@strawberry.type
class CourseType:
    id: uuid.UUID
    title: str
    description: str
    status: str