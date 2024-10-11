# src/graphql/index.py

import strawberry
from src.graphql.land.mutation import LandMutation
from src.graphql.land.query import LandQuery
from src.graphql.users import UserQuery, UserMutation

@strawberry.type
class Mutation(LandMutation, UserMutation):
    pass

@strawberry.type
class Query(LandQuery, UserQuery):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
    