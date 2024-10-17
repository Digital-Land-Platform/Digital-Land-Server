# src/graphql/index.py

import strawberry
from src.graphql.land.mutation import LandMutation
from src.graphql.land.query import LandQuery
from .users.mutation import UserMutation
from .users.query import UserQuery

@strawberry.type
class Mutation(UserMutation, LandMutation):
    pass

@strawberry.type
class Query(UserQuery, LandQuery):
    pass