from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship, validates
from src.models.Base import Base
class Image(Base):
    __tablename__ = "images"
    

    url = Column(String, nullable=False)
    property_id = Column(UUID, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)


    @validates('url')
    def check_image_urls(self, key, value):
        if value is not None and not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError('Each image URL must start with http:// or https://.')
        return value