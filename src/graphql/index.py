# src/graphql/index.py

import strawberry
from src.graphql.users.mutation import UserMutation
from src.graphql.property.mutation import PropertyMutation
from src.graphql.property.query import PropertyQuery 
from src.graphql.users.query import UserQuery
from src.graphql.userProfile.mutation import UserProfileMutation
from src.graphql.userProfile.query import UserProfile
from src.graphql.amenity.mutation import AmenityMutation
from src.graphql.amenity.query import AmenityQuery

@strawberry.type
class Mutation(UserMutation, UserProfileMutation, PropertyMutation, AmenityMutation):
    pass

@strawberry.type
class Query(UserQuery, UserProfile, PropertyQuery, AmenityQuery):
    pass