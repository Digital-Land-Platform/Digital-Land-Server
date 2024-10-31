import strawberry
from typing import Optional
from uuid import UUID
from strawberry.file_uploads import Upload

@strawberry.input
class ImageInput:
    #property_id: UUID
    file: Optional[Upload] = None 
    url: Optional[str] = None
    
@strawberry.input
class ImageUpdateInput:
    image_id: UUID
    file: Optional[Upload] = None 
    url: Optional[str] = None
@strawberry.type
class ImageType:
    id: Optional[UUID] = None
    url: Optional[str] = None
    property_id: UUID
    
