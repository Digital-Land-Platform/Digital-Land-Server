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
from .certification.mutation import CertificationMutation
from .certification.query import CertificationQuery
from .notableclient.query import NotableClientQuery
from .notableclient.mutation import NotableClientMutation
from .organization.query import OrganizationQuery
from .organization.mutation import OrganizationMutation
from .organizationProfile.mutation import OrganizationProfileMutation
from .organizatoinStaff.mutation import OrganizationStaffMutation
from .organizatoinStaff.query import OrganizationStaffQuery
from .invitation.query import InvitationQuery
from .invitation.mutation import InvitationMutation


@strawberry.type

class Mutation(UserMutation, UserProfileMutation, PropertyMutation, AmenityMutation,ImageMutation,
               CertificationMutation, NotableClientMutation, OrganizationMutation, OrganizationProfileMutation,
               OrganizationStaffMutation, InvitationMutation):
    pass

@strawberry.type
class Query(UserQuery, UserProfile, PropertyQuery, AmenityQuery, LocationQuery,
            CertificationQuery, NotableClientQuery, ImageQuery, OrganizationQuery, OrganizationStaffQuery,
            InvitationQuery):
    pass