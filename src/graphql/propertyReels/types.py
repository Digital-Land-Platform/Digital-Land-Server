import strawberry
from uuid import UUID
from strawberry.file_uploads import Upload
from typing import Optional

@strawberry.type
class ReelType:
    id: UUID
    property_id: UUID
    creator_id: UUID
    title: str
    description: str
    url: str

@strawberry.input
class ReelCreateInput:
    title: str
    #creator_id: UUID
    #property_id: UUID
    description: str
    file: Upload 

@strawberry.input
class ReelUpdateInput:
    title: Optional[str] = None
    description: Optional[str] = None
    file: Optional[Upload] = None
    creator_id: Optional[UUID] = None
  


