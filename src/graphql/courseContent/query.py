import strawberry
from .services import CourseContentService
from typing import List
from .types import ContentType
import uuid
from config.database import db
from .types import CourseContentType

service = CourseContentService(db)

@strawberry.type
class ContentQuery:
    @strawberry.field
    async def get_content(self, content_id: uuid.UUID) -> CourseContentType:
        content = await service.get_content_by_id(content_id)
        return content
    
    @strawberry.field
    async def get_all_contents(self) -> List[CourseContentType]:
        contents = await service.get_all_contents()
        return contents
    
    
