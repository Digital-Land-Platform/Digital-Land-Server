from fastapi import HTTPException
import strawberry
from strawberry.types import Info
from src.middleware.ErrorHundlers.ExceptionHundler import ExceptionHandler
from src.models.enums.UserRole import UserRole
from src.middleware.UserProfileValidator import UserProfileValidator
from .types import OrganizationType, OrganizationInput
from .service import OrganizationService
from src.middleware.AuthManagment import AuthManagement
from config.database import db
from src.graphql.organizatoinStaff.types import OrganizationStaffType

auth_management = AuthManagement()
organization_service = OrganizationService(db)

@strawberry.type
class OrganizationMutation:

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def create_organization(self, info: Info, organization_data: OrganizationInput) -> OrganizationType:
        token = info.context["request"].headers.get("Authorization").split(" ")[1]
        user_info = auth_management.get_user_info(token)
        organization_data = vars(organization_data)
        organization = await organization_service.create_organization(organization_data, user_info.get("email"))
        return OrganizationType.from_orm(organization)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def update_organization(self, info: Info, org_id: str, org_data: OrganizationInput) -> OrganizationType:
        org_data = vars(org_data)
        if org_data.get("issue_date"):
            org_data["issue_date"] = UserProfileValidator.change_str_date(org_data.get("issue_date"), "issue_date")
        else:
            org_data.pop("issue_date")

        if org_data.get("expiration_date"):
            org_data["expiration_date"] = UserProfileValidator.change_str_date(org_data.get("expiration_date"), "expiration_date")
        else:
            org_data.pop("expiration_date")

        organization = await organization_service.update_organization(org_id, org_data)
        return OrganizationType.from_orm(organization)

    @strawberry.mutation
    @auth_management.isAuth()
    @ExceptionHandler.handle_exceptions
    async def delete_organization(self, info, org_id: str) -> str:
        message = await organization_service.delete_organization(org_id)
        return message
