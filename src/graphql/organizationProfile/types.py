import strawberry


@strawberry.type
class OrganizationProfileType:
    id: str | None
    organization_id: str | None
    mission_statement: str | None
    vision: str | None
    values: str | None
    description: str | None
    industry: str | None
    year_founded: int | None
    headquarters: str | None
    num_employees: int | None
    annual_revenue: float | None
    website_url: str | None
    logo_url: str | None

    @classmethod
    def from_orm(cls, organization_profile):
        return cls(
            id=organization_profile.id,
            organization_id=organization_profile.organization_id,
            mission_statement=organization_profile.mission_statement,
            vision=organization_profile.vision,
            values=organization_profile.values,
            description=organization_profile.description,
            industry=organization_profile.industry,
            year_founded=organization_profile.year_founded,
            headquarters=organization_profile.headquarters,
            num_employees=organization_profile.num_employees,
            annual_revenue=organization_profile.annual_revenue,
            website_url=organization_profile.website_url,
            logo_url=organization_profile.logo_url
        )


@strawberry.input
class OrganizationProfileInput:
    organization_id: str | None
    mission_statement: str | None = None
    vision: str | None = None
    values: str | None = None
    description: str | None = None
    industry: str | None = None
    year_founded: int | None = None
    headquarters: str | None = None
    num_employees: int | None = None
    annual_revenue: float | None = None
    website_url: str | None = None
    logo_url: str | None = None