# src/graphql/land/query.py

import strawberry

from strawberry.types import Info

@strawberry.type
class LandQuery:
    @strawberry.field
    def dummy_query(self, info: Info) -> str:
        return "Dummy query response"