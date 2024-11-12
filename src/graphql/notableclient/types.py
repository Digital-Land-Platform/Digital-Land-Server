import strawberry


@strawberry.type
class NotableClientType:
    id: str | None
    client_name: str | None
    industry: str | None
    logo_url: str | None

    @classmethod
    def from_model(cls, notable_client):
        return NotableClientType(
            id=notable_client.id,
            client_name=notable_client.client_name,
            industry=notable_client.industry,
            logo_url=notable_client.logo_url
        )

@strawberry.input
class NotableClientInput:
    client_name: str | None
    industry: str | None
    logo_url: str | None = None