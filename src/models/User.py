from sqlalchemy import Boolean, Column, DateTime, String, Enum
from sqlalchemy.sql import func
from .enums.UserRole import UserRole
from .enums.AccountStatus import AccountStatus
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.models.UserProfile import UserProfile
from src.models.TwoFactorAuth import TwoFactorAuth
from src.models.OrganizationStaff import OrganizationStaff
from src.models.Transaction import Transaction
from src.models.Notification import Notification
from src.models.Message import Message
from src.models.Reel import Reel
from src.models.Course import Course
from .Base import Base
from .Property import Property
from .Availability import Availability

class User(Base):
    __tablename__ = "users"
    image = Column(String)
    username = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), nullable=True)
    phone_number = Column(String)
    is_2FA_enabled = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.INACTIVE)
    last_login = Column(DateTime(timezone=True), server_default=func.now())

    availability = relationship("Availability", backref="users", cascade="all, delete, delete-orphan")
    user_profile = relationship("UserProfile", backref="users", cascade="all, delete, delete-orphan")
    two_factor_auth = relationship("TwoFactorAuth", backref="users", cascade="all, delete, delete-orphan")
    notification = relationship("Notification", backref="users", cascade="all, delete, delete-orphan")
    reel = relationship("Reel", backref="users", cascade="all, delete, delete-orphan")
    course_created = relationship("Course", backref="users", cascade="all, delete, delete-orphan")
    message_sender = relationship("Message", 
                                primaryjoin="User.id == Message.sender_id", 
                                backref="sender", 
                                cascade="all, delete, delete-orphan")
    message_reciever = relationship("Message", 
                                      primaryjoin="User.id == Message.receiver_id", 
                                      backref="reciever", 
                                      cascade="all, delete, delete-orphan")
    transactions = relationship("Transaction", 
                                primaryjoin="User.id == Transaction.buyer_id", 
                                backref="buyer", 
                                cascade="all, delete, delete-orphan")
    transactions_sold = relationship("Transaction", 
                                      primaryjoin="User.id == Transaction.seller_id", 
                                      backref="seller", 
                                      cascade="all, delete, delete-orphan")
    transactions_verified = relationship("Transaction", 
                                          primaryjoin="User.id == Transaction.notary_id", 
                                          backref="notary", 
                                          cascade="all, delete, delete-orphan")
    properties = relationship("Property", backref="users", cascade="all, delete, delete-orphan")
