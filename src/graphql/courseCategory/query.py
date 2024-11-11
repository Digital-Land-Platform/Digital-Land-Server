import strawberry
from .services import CourseCategoryService
from .types import CourseCategoryType
from config.database import db
from typing import Optional, List
import uuid
from uuid import UUID

category_service = CourseCategoryService(db.SessionLocal())

@strawberry.type
class CourseCategoryQuery:
    @strawberry.field
    async def get_all_categories(self) -> List[CourseCategoryType]:
        """Get all categories"""
        return await category_service.get_all_categories()
    
    @strawberry.field
    async def get_category_by_id(self, category_id: UUID) -> CourseCategoryType:
        """Get category by id"""
        return await category_service.get_category_by_id(category_id)
