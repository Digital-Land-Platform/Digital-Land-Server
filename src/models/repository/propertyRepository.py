from uuid import UUID
from typing import Optional
from sqlalchemy.future import select
from src.models.Owner import Owner
from src.models.Property import Property
from config.database import DatabaseSession

class PropertyRepository:
    def __init__(self):
        self.db = DatabaseSession()

    async def create_owner(self, name: str, contact_info: str, address: str = None):
        new_owner = Owner(
            name=name, 
            contact_info=contact_info,
            address=address
            )
        async with self.db:
            async with self.db.session as session:
                session.add(new_owner)
                await session.commit()
                await session.refresh(new_owner)
        return new_owner

    async def update_owner(self, id: UUID, name: str = None, contact_info: str = None, address: str = None):
        async with self.db:
            async with self.db.session as session:
                owner = await session.get(Owner, id)
                if owner is None:
                    return None
                if name is not None:
                    owner.name = name
                if contact_info is not None:
                    owner.contact_info = contact_info
                if address is not None:
                    owner.address = address
                await session.commit()
                await session.refresh(owner)
        return owner

    async def delete_owner(self, id: UUID):
        async with self.db:
            async with self.db.session as session:
                owner = await session.get(Owner, id)
                if owner is not None:
                    await session.delete(owner)
                    await session.commit()
                    return True
                return False

    async def create_property(self, title: str, description: str, price: float, size: float,
                              location: str, neighborhood: str, city: str, country: str,
                              legalStatus: str, images: str, owner_id: UUID, status: str = "available"):
        new_property = Property(
            title=title,
            description=description,
            price=price,
            size=size,
            location=location,
            neighborhood=neighborhood,
            city=city,
            country=country,
            owner_id=owner_id,
            status=status,
            images=images,
            legalStatus=legalStatus
        )
        async with self.db:
            async with self.db.session as session:
                session.add(new_property)
                await session.commit()
                await session.refresh(new_property)
        return new_property

    async def update_property(
        self,
        id: UUID,
        title: str,
        description: str,
        price: float,
        size: float,
        status: str,
        location: str,
        neighborhood: str,
        city: str,
        country: str,
        legalStatus: str,
        images: list[str]
    ) -> Optional[Property]:
        async with self.db:
            async with self.db.session as session:
                property_ = await session.get(Property, id)
                if property_ is None:
                    return None

                # Update fields explicitly
                property_.title = title
                property_.description = description
                property_.price = price
                property_.size = size
                property_.status = status
                property_.location = location
                property_.neighborhood = neighborhood
                property_.city = city
                property_.country = country
                property_.legalStatus = legalStatus
                property_.images = images

                await session.commit()
                await session.refresh(property_)

        return property_


    async def delete_property(self, id: UUID):
        async with self.db:
            async with self.db.session as session:
                property_ = await session.get(Property, id)
                if property_ is not None:
                    await session.delete(property_)
                    await session.commit()
                    return True
                return False

    async def get_owner(self, id: UUID):
        async with self.db:
            async with self.db.session as session:
                return await session.get(Owner, id)

    async def get_property(self, id: UUID):
        async with self.db:
            async with self.db.session as session:
                return await session.get(Property, id)

    async def list_owners(self):
        async with self.db:
            async with self.db.session as session:
                owners = await session.execute(select(Owner))
                return owners.scalars().all()

    async def list_properties(self):
        async with self.db:
            async with self.db.session as session:
                properties = await session.execute(select(Property))
                return properties.scalars().all()
