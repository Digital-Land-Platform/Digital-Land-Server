import enum
import strawberry

@strawberry.enum
class ContentType(enum.Enum):
    VIDEO = "Video"
    ARTICLE = "Article"
    QUIZ = "Quiz"
    REEL = "Reel"