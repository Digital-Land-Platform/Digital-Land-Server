from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.models.PropertyCatagoryRelation import PropertyCatagoryRelation
from src.models.Property import Property
from sqlalchemy.dialects.postgresql import UUID

class PropertyCatagoryRelationRepository:

    def __init__(self, db):
        self.db = db
    
    async def create_relation(self, relation: PropertyCatagoryRelation) -> PropertyCatagoryRelation:
        try:
            async with self.db:
                async with self.db.session as session:
                    session.add(relation)
                    await session.commit()
                    await session.refresh(relation)
                    return relation
        except Exception as e:
            raise Exception(f"Error creating relation: {e}")
    
    async def update_relation(self, relation_id: str, relation_data: dict) -> PropertyCatagoryRelation:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagoryRelation).where(PropertyCatagoryRelation.id == relation_id)
                    )
                    relation = result.scalar_one_or_none()
                    for key, value in relation_data.items():
                        if value and hasattr(relation, key):
                            setattr(relation, key, value)
                    session.add(relation)
                    await session.commit()
                    await session.refresh(relation)
                    return relation
        except Exception as e:
            raise Exception(f"Error updating relation: {e}")
    
    async def get_relation(self, relation_id: str) -> PropertyCatagoryRelation:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagoryRelation).where(PropertyCatagoryRelation.id == relation_id)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting relation: {e}")
    
    async def get_relation_by_property_id(self, property_id: str) -> List[PropertyCatagoryRelation]:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagoryRelation).where(PropertyCatagoryRelation.property_id == property_id)
                    )
                    return result.scalars().all()
        except Exception as e:
            raise Exception(f"Error getting relation: {e}")
    
    async def get_relation_by_catagory_id(self, catagory_id: str) -> PropertyCatagoryRelation:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagoryRelation).where(PropertyCatagoryRelation.catagory_id == catagory_id)
                    )
                    return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting relation: {e}")
    
    async def delete_relation(self, relation_id: str) -> str:
        try:
            async with self.db:
                async with self.db.session as session:
                    result = await session.execute(
                        select(PropertyCatagoryRelation).where(PropertyCatagoryRelation.id == relation_id)
                    )
                    relation = result.scalar_one_or_none()
                    await session.delete(relation)
                    await session.commit()
                    return "Relation deleted successfully"
        except Exception as e:
            raise Exception(f"Error deleting relation: {e}")
    
    async def get_properties_by_category_id(self, category_id: UUID) -> List[Property]:
        try:
            async with self.db as session:
                result = await session.execute(
                    select(PropertyCatagoryRelation.property_id)
                    .where(PropertyCatagoryRelation.catagory_id == category_id)
                )
                property_ids = result.scalars().all()
                
                if property_ids:
                    properties_result = await session.execute(
                        select(Property)
                        .options(joinedload(Property.images), joinedload(Property.amenities))
                        .where(Property.id.in_(property_ids))
                    )
                    properties = properties_result.scalars().unique()
                    return properties.all() if properties else []
                return []
        except Exception as e:
            raise Exception(f"Error fetching properties by category ID: {e}")

