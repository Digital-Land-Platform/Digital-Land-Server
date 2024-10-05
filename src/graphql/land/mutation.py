# src/graphql/land/mutation.py

import strawberry

@strawberry.type
class LandMutation:
    @strawberry.mutation
    def dummy_mutation(self, info) -> str:
        return "Dummy mutation response"