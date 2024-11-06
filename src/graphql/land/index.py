# src/graphql/land/index.py
import strawberry
from .query import PropertyQuery
from .mutation import PropertyMutation

@strawberry.type
class Query(PropertyQuery):
    pass

@strawberry.type
class Mutation(PropertyMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
