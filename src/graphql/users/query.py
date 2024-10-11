# src/graphql/land/mutation.py

import strawberry
from src.graphql.users.types import UserType
from src.models import User  
from config.database import db  
from strawberry.types import Info


@strawberry.type
class UserQuery:
    @strawberry.field
    async def users(self, info: Info) -> list[UserType]:
        async for session in db.get_db():
            users = session.query(User).all()  # Fetch all users
            return [UserType(id=user.id, name=user.name, email=user.email, role=user.role.value) for user in users]
