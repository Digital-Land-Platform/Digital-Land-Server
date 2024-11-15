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
from src.graphql.certification.mutation import CertificationMutation
from src.graphql.certification.query import CertificationQuery
from src.graphql.notableclient.query import NotableClientQuery
from src.graphql.notableclient.mutation import NotableClientMutation
from src.graphql.organization.query import OrganizationQuery
from src.graphql.organization.mutation import OrganizationMutation
from src.graphql.organizationProfile.mutation import OrganizationProfileMutation
from src.graphql.organizatoinStaff.mutation import OrganizationStaffMutation
from src.graphql.organizatoinStaff.query import OrganizationStaffQuery
from src.graphql.invitation.query import InvitationQuery
from src.graphql.invitation.mutation import InvitationMutation
from src.graphql.organizationProfile.query import OrganizationProfileQuery
from src.graphql.propertyReels.mutation import ReelMutation
from src.graphql.propertyReels.query import ReelQuery
from src.graphql.propertySearch.query import PropertySearchQuery
from src.graphql.transaction.query import TransactionQuery
from src.graphql.transaction.mutation import TransactionMutation
from src.graphql.message.query import MessageQuery
from src.graphql.message.mutation import MessageMutation
from src.graphql.payment.query import PaymentQuery
from src.graphql.payment.mutation import PaymentMutation

@strawberry.type

class Mutation(UserMutation, UserProfileMutation, PropertyMutation, AmenityMutation,ImageMutation,
               CertificationMutation, NotableClientMutation, OrganizationMutation, OrganizationProfileMutation,
               OrganizationStaffMutation, InvitationMutation, ReelMutation, CourseContentMutation, CourseMutation, CourseCategoryMutation,
               PaymentMutation, TransactionMutation, MessageMutation):
    pass

@strawberry.type
class Query(UserQuery, UserProfile, PropertyQuery, AmenityQuery, LocationQuery,
            CertificationQuery, NotableClientQuery, ImageQuery, OrganizationQuery, OrganizationStaffQuery,
            InvitationQuery, OrganizationProfileQuery, PropertySearchQuery, ReelQuery,  ContentQuery, CourseQuery, CourseCategoryQuery, 
            PaymentQuery, TransactionQuery, MessageQuery):
    pass