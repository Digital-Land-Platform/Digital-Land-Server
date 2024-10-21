# src/graphql/index.py

import strawberry
from src.graphql.users.mutation import UserMutation
# from src.graphql.land.mutation import LandMutation
# from src.graphql.land.query import LandQuery
from src.graphql.property.mutation import PropertyMutation
from src.graphql.property.query import PropertyQuery 
from src.graphql.users.query import UserQuery

@strawberry.type
class Mutation(UserMutation, PropertyMutation):
    pass

@strawberry.type
class Query(UserQuery, PropertyQuery):
    pass