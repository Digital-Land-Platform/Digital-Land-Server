import json
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from config.database import db
from src.models.Organization import Organization
from src.models.OrganizationProfile import OrganizationProfile
from src.middleware.UserProfileValidator import UserProfileValidator
from src.models.repository.OrganizationRepository import OrganizationRepository
from src.models.repository.OrganizationProfileRepository import OrganizationProfileRepository

class OrganizationSeeder:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.org_repostiory = OrganizationRepository(db)
        self.org_profile_repository = OrganizationProfileRepository(db)

    async def seed_organizations_from_json(self):
        current_dir = os.path.dirname(__file__)

        file_path = os.path.join(current_dir, "files", "organizations.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "r") as file:
            organizations = json.load(file)

        for org_data in organizations:
            org_data["issue_date"] = UserProfileValidator.change_str_date(org_data["issue_date"])
            org_data["expiration_date"] = UserProfileValidator.change_str_date(org_data["expiration_date"])
            org_data["verification_date"] = UserProfileValidator.change_str_date(org_data["verification_date"])
            profile = org_data.pop("profile")
            organizations = await self.org_repostiory.create_organization(Organization(**org_data))
            profile["organization_id"] = organizations.id
            org_profile = await self.org_profile_repository.create_organization_profile(OrganizationProfile(**profile))
            # # Create Organization
            # organization = Organization(
            #     name=org_data["name"],
            #     TIN=org_data["TIN"],
            #     issue_date=issue_date,
            #     expiration_date=expiration_date,
            #     is_verified=org_data["is_verified"],
            #     verification_date=verification_date,
            # )
            # db.add(organization)
            # db.commit()
            # db.refresh(organization)

            # # Create Organization Profile
            # profile_data = org_data["profile"]
            # organization_profile = OrganizationProfile(
            #     organization_id=organization.id,
            #     mission_statement=profile_data["mission_statement"],
            #     vision=profile_data["vision"],
            #     values=profile_data["values"],
            #     description=profile_data["description"],
            #     industry=profile_data["industry"],
            #     year_founded=profile_data["year_founded"],
            #     headquarters=profile_data["headquarters"],
            #     num_employees=profile_data["num_employees"],
            #     annual_revenue=profile_data["annual_revenue"],
            #     website_url=profile_data["website_url"],
            #     logo_url=profile_data["logo_url"],
            # )
            # db.add(organization_profile)

        # db.commit()
            #print(f"Seeded {org_data.pop("profile")} organizations from {json_file}.")
