import strawberry
from src.graphql.users.query import UserQuery
from src.graphql.users.mutation import UserMutation

schema = strawberry.Schema(query=UserQuery, mutation=UserMutation)
