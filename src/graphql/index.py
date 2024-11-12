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
from src.graphql.image.mutation import ImageMutation
from src.graphql.image.query import ImageQuery
from .location.query import LocationQuery
from src.graphql.courseContent.mutation import CourseContentMutation
from src.graphql.courseContent.query import ContentQuery
from src.graphql.course.mutation import CourseMutation
from src.graphql.course.query import CourseQuery
from src.graphql.courseCategory.mutation import CourseCategoryMutation
from src.graphql.courseCategory.query import CourseCategoryQuery
from src.graphql.propertySearch.query import PropertySearchQuery

@strawberry.type
class Mutation(UserMutation, UserProfileMutation, PropertyMutation, AmenityMutation, ImageMutation, CourseContentMutation, CourseMutation, CourseCategoryMutation):
    pass

@strawberry.type
class Query(UserQuery, UserProfile, PropertyQuery, AmenityQuery, ImageQuery, LocationQuery, ContentQuery, CourseQuery, CourseCategoryQuery, PropertySearchQuery):
    pass