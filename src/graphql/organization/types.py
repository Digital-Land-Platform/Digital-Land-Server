import strawberry

def class_call():
    from src.graphql.organizatoinStaff.types import OrganizationStaffInput
    return OrganizationStaffInput

@strawberry.type
class OrganizationType:
    id: str| None
    name: str | None
    TIN: str | None
    issue_date: str | None
    expiration_date: str | None
    verification_date: str | None

    @classmethod
    def from_orm(cls, organization):
        return cls(
            id=organization.id,
            name=organization.name,
            TIN=organization.TIN,
            issue_date=organization.issue_date.isoformat(),
            expiration_date=organization.expiration_date.isoformat() if organization.expiration_date else None,
            verification_date=organization.verification_date.isoformat() if organization.verification_date else None
        )

@strawberry.input
class OrganizationInput(class_call()):
    name: str | None = None
    TIN: str | None = None
    issue_date: str | None = None
    expiration_date: str | None = None