from src.graphql.userProfile.types import UserProfileType
from src.graphql.organization.types import OrganizationType
from src.models.repository.UserProfileRepository import UserProfileRepository
from src.models.repository.OrganizationRepository import OrganizationRepository
from enum import Enum
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

@strawberry.type
class OrganizationStaffType(UserProfileType, OrganizationType):
    id: str | None
    organization_id: str | None
    start_date: str | None
    end_date: str | None
    role: str | None

    @classmethod
    async def from_orm(cls, db: AsyncSession, organization_staff):
        user_profile_repo = UserProfileRepository(db)
        organization_repo = OrganizationRepository(db)
        user_profile =await user_profile_repo.get_user_profile_by_id(organization_staff.user_id)
        organization =await organization_repo.get_organization(organization_staff.organization_id)
        return cls(
            id=organization_staff.id,
            user_id=user_profile.user_id,
            organization_id=organization_staff.organization_id,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            gender=user_profile.gender,
            date_of_birth=user_profile.date_of_birth.isoformat(),
            location_id=user_profile.location_id,
            license_number=user_profile.license_number,
            name=organization.name,
            TIN=organization.TIN,
            issue_date=organization.issue_date.isoformat(),
            expiration_date=organization.expiration_date.isoformat() if organization.expiration_date else None,
            verification_date=organization.verification_date.isoformat() if organization.verification_date else None,
            role=organization_staff.role.value,
            start_date=organization_staff.start_date.isoformat() if organization_staff.start_date else None,
            end_date=organization_staff.end_date.isoformat() if organization_staff.end_date else None
        )

@strawberry.enum
class OrganizationStaffRole(Enum):
    OWNER = "Owner"
    CEO = "CEO"
    CTO = "CTO"
    CFO = "CFO"
    COO = "COO"
    MANAGER = "Manager"
    ADMIN = "Admin"
    TEAM_LEAD = "Team Lead"
    SENIOR_EMPLOYEE = "Senior Employee"
    JUNIOR_EMPLOYEE = "Junior Employee"
    INTERN = "Intern"
    CONSULTANT = "Consultant"
    CONTRACTOR = "Contractor"
    TEMPORARY_STAFF = "Temporary Staff"
    HR_REPRESENTATIVE = "HR Representative"
    MARKETING_SPECIALIST = "Marketing Specialist"
    SALES_REPRESENTATIVE = "Sales Representative"
    ACCOUNTANT = "Accountant"
    PRODUCT_MANAGER = "Product Manager"
    PROJECT_MANAGER = "Project Manager"
    CUSTOMER_SUPPORT = "Customer Support"

@strawberry.input
class OrganizationStaffInput:
    organization_id: str | None = None
    user_id: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    role: OrganizationStaffRole | None = None

