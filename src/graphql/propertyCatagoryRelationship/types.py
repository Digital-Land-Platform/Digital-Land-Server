import strawberry

@strawberry.type
class PropertyCatagoryRelationshipType:
    id: str
    property_id: str
    catagory_id: str

    @classmethod
    def from_orm(cls, catagory):
        return cls(
            id=str(catagory.id),
            property_id=catagory.property_id,
            catagory_id=catagory.catagory_id
        )


@strawberry.input
class PropertyCatagoryRelationshipInput:
    property_id: str
    catagory_id: str

@strawberry.input
class UpdatePropertyCatagoryRelationship:
    property_id: str | None = None
    catagory_id: str | None = None