import strawberry
from src.models.User import UserRole

@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    role: UserRole

@strawberry.input
class CreateUserInput:
    name: str
    email: str
    password: str
    role: UserRole
