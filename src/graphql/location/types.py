import strawberry

@strawberry.type
class LocationType:
    id: str | None
    province: str | None
    district: str | None
    sector: str | None
    cell: str | None
    village: str | None
    city: str | None
    country: str | None

    @classmethod
    def from_model(cls, location):
        return LocationType(
            id=location.id,
            province=location.province,
            district=location.district,
            sector=location.sector,
            cell=location.cell,
            village=location.village,
            city=location.city,
            country=location.country
        )
