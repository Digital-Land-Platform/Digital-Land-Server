# src/graphql/index.py

import strawberry
from src.graphql.land.mutation import LandMutation
from src.graphql.land.query import LandQuery

@strawberry.type
class Mutation(LandMutation):
    pass

@strawberry.type
class Query(LandQuery):
    pass