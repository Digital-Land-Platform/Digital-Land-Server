import strawberry


@strawberry.type
class CertificationType:
    id: str | None
    certification_name: str | None
    issued_by: str | None
    certificate_url: str | None = None

    @classmethod
    def from_model(cls, certification):
        return CertificationType(
            id=certification.id,
            certification_name=certification.certification_name,
            issued_by=certification.issued_by,
            certificate_url=certification.certificate_url
        )


@strawberry.input
class CertificationBaseInput:
    certification_name: str | None
    issued_by: str | None
    certificate_url: str | None = None