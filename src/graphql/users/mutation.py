import strawberry
from .schemas import UserType, CreateUserInput
from .resolvers import create_user
from .database import SessionLocal

@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def register_user(self, input: CreateUserInput) -> UserType:
        db = SessionLocal()
        user = await create_user(input, db)
        return user

schema = strawberry.Schema(mutation=Mutation)
