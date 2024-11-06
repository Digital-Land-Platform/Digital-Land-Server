import enum
import strawberry

@strawberry.enum
class CourseCategory(enum.Enum):
    REAL_ESTATE = "Real Estate"
    PROPERTY_MANAGEMENT = "Property Management"
    PLATFORM_USAGE = "Platform Usage"
    EDUCATIONAL = "Educational"