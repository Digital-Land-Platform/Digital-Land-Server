from sqlalchemy import Column, Enum, Integer, String, Float, ForeignKey
from sqlalchemy import Table, Text
from src.models.Amenity import Amenity
from src.models.Image import Image
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
from src.models.Base import Base, BaseModel
from src.models.Reel import Reel
from src.models.enums.PropertyStatus import PropertyStatus
from src.models.PropertyCatagoryRelation import PropertyCatagoryRelation


class Property(Base):
    __tablename__ = "properties"
    
    title = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(String)
    price = Column(Float)
    size = Column(Float)
    status = Column(Enum(PropertyStatus), default=PropertyStatus.PENDING)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))
    neighborhood = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    year_built = Column(Integer)
    legal_status = Column(String)
    disclosure = Column(String)
    energy_rating = Column(String)
    street_view_url = Column(String)
    future_development_plans = Column(Text, nullable=True)
    zoning_information = Column(Text, nullable=True)
    property_amenities = Table("property_amenities", Base.metadata,
                              Column("property_id", UUID(as_uuid=True),
                                     ForeignKey("properties.id", ondelete="CASCADE"),
                                     nullable=False),
                              Column("amenity_id", UUID(as_uuid=True),
                                     ForeignKey("amenities.id", ondelete="CASCADE"),
                                     nullable=False),
                              mysql_charset="latin1",)
    
    amenities = relationship("Amenity", secondary=property_amenities,
                                 viewonly=False, lazy="joined")
    transaction = relationship("Transaction", backref="properties", cascade="all, delete, delete-orphan")
    message = relationship("Message", backref="properties", cascade="all, delete, delete-orphan")
    reels = relationship("Reel", backref="properties", cascade="all, delete, delete-orphan")
    images = relationship("Image", backref="properties", cascade="all, delete-orphan", lazy="joined")
    property_catagories = relationship("PropertyCatagoryRelation", backref="properties")

    @validates('price')
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        return value

    @validates('size')
    def validate_size(self, key, value):
        if value <= 0:
            raise ValueError("Size must be positive")
        return value
    
    @validates('yearBuilt')
    def check_year_built(self, key, value):
        if value is not None and value < 0:
            raise ValueError('Year built must be a non-negative integer.')
        return value
    
