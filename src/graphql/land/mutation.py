# src/graphql/land/mutation.py

import strawberry

from strawberry.types import Info

@strawberry.type
class LandMutation:
    @strawberry.mutation
    def dummy_mutation(self, info: Info) -> str:
        return "Dummy mutation response"