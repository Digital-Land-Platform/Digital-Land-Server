# src/graphql/land/query.py

import strawberry

@strawberry.type
class LandQuery:
    @strawberry.field
    def dummy_query(self, info) -> str:
        return "Dummy query response"