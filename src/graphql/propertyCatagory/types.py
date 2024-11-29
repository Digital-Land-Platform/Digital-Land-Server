import strawberry

@strawberry.type
class PropertyCatagoryType:
    id: str
    name: str
    description: str

    @classmethod
    def from_orm(cls, catagory):
        return cls(
            id=str(catagory.id),
            name=catagory.name,
            description=catagory.description
        )


@strawberry.input
class PropertyCatagoryInput:
    name: str
    description: str

@strawberry.input
class UpdatePropertyCatagory:
    name: str | None = None
    description: str | None = None