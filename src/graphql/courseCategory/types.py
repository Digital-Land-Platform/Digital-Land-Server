import strawberry
from typing import Optional
import uuid

@strawberry.input
class CourseCategoryCreateInput:
    name: str

@strawberry.input
class CourseCategoryUpdateInput:
    id: uuid.UUID
    name: Optional[str] = None

@strawberry.type
class CourseCategoryType:
    id: uuid.UUID
    name: str
