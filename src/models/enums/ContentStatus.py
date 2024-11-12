import enum
import strawberry

@strawberry.enum
class ContentStatus(enum.Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"
