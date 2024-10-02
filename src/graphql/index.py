import strawberry

# from src.graphql.ride.query import RideQuery
# from src.graphql.ride.mutation import RideMutation
from src.graphql.land.mutation import LandMutation
from src.graphql.land.query import LandQuery
from src.graphql.users.mutation import UserMutation
# from src.graphql.routes.query import RouteQuery
# from src.graphql.routes.mutation import RouteMutation
from src.graphql.users.query import UserQuery

# Import all queries and mutations


# Merge queries and mutations from different modules
@strawberry.type
class Query(LandQuery, UserQuery):
    pass


@strawberry.type
class Mutation(LandMutation, UserMutation):
    pass

