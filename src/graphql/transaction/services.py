from datetime import datetime, timedelta
from config.logging import logger
from enum import Enum
import random
from src.middleware.ErrorHundlers.CustomErrorHandler import ( 
    BadRequestException, InternalServerErrorException, NotFoundException 
    )
from src.models.repository.TransactionRepository import TransactionRepository
from src.models.Transaction import Transaction
from src.models.enums.TransactionType import TransactionType
from src.models.enums.TransactionStatus import TransactionStatus
from src.graphql.property.services import PropertyService
from src.graphql.users.services import UserService
from src.graphql.userProfile.service import UserProfileService
from src.graphql.location.service import LocationService
from src.models.enums.UserRole import UserRole
from src.graphql.message.services import MessageService
from src.models.Message import Message
from config.database import db
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.utility import Utility
from src.models.enums.PropertyStatus import PropertyStatus


class TransactionService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.transaction_repo = TransactionRepository(self.db)
        self.property_service = PropertyService(self.db.SessionLocal())
        self.user_service = UserService(self.db)
        self.user_profile_service = UserProfileService(self.db)
        self.location_service = LocationService(self.db)
        self.message_service = MessageService(self.db)

    async def create_transaction(self, new_transaction: Dict) -> Transaction:
        try:
            if "transaction_type" in new_transaction and new_transaction.get("transaction_type"):
                transaction_type = new_transaction.get("transaction_type").name
                new_transaction["transaction_type"] = getattr(TransactionType, transaction_type, None)
                if new_transaction["transaction_type"] is None:
                    raise BadRequestException(f"Invalid Transaction type: {transaction_type}")
                
            if "status" in new_transaction and new_transaction.get("status"):
                status_type = new_transaction.get("status").name
                new_transaction["status"] = getattr(TransactionStatus, status_type, None)
                if new_transaction["status"] is None:
                    raise BadRequestException(f"Invalid status: {status_type}")
            else:
                new_transaction["status"] = TransactionStatus.PENDING
            property = await self.property_service.get_property(new_transaction["property_id"])
            if not property:
                raise NotFoundException("Property not found")
            await self.property_service.change_user_status(property.id, {"status": PropertyStatus.PENDING})
            seller = await self.user_service.get_user_by_id(property.user_id)
            if not seller:
                raise NotFoundException("Seller not found")
            new_transaction["seller_id"] = property.user_id
            users = await self.user_service.get_all_users()
            if not users:
                raise NotFoundException("No users found")
            seller_location_id = await self.user_profile_service.get_user_profile_by_user_id(seller.id)
            seller_location = await self.location_service.get_location_by_id(seller_location_id.location_id)
            property_location = await self.location_service.get_location_by_id(property.location_id)
            eligible_notaries = []
            for user in users:
                notary_profile = await self.user_profile_service.get_user_profile_by_user_id(str(user.id))
                notary_location = await self.location_service.get_location_by_id(notary_profile.location_id)
                if user.role == UserRole.NOTARY and notary_location.province\
                        == property_location.province == seller_location.province:
                    eligible_notaries.append(user.id)
            if len(eligible_notaries) > 0:
                new_transaction["notary_id"] = random.choice(eligible_notaries)
            new_transaction["transaction_number"] = await Utility.generate_transaction_number()
            new_transaction["amount"] = property.price
            new_transaction["transaction_date"] = datetime.now()
            new_transaction["payment_due_date"] = datetime.now() + timedelta(days=2)
            transaction = await self.transaction_repo.create_transaction(Transaction(**new_transaction))
            return transaction
        except BadRequestException as e:
            raise e
        except NotFoundException as e:
            raise e
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise InternalServerErrorException(f"{e}")
    
    async def update_transaction(self, transaction_id: str, transaction_data: Dict) -> Transaction:
        try:
            if "transaction_type" in transaction_data and transaction_data.get("transaction_type"):
                transaction_type = transaction_data.get("transaction_type").name
                transaction_data["transaction_type"] = getattr(TransactionType, transaction_type, None)
                if transaction_data["transaction_type"] is None:
                    raise BadRequestException(f"Invalid Transaction type: {transaction_type}")
                
            if "status" in transaction_data and transaction_data.get("status"):
                status_type = transaction_data.get("status").name
                transaction_data["status"] = getattr(TransactionStatus, status_type, None)
                if transaction_data["status"] is None:
                    raise BadRequestException(f"Invalid status: {status_type}")
            if "property_id" in transaction_data and transaction_data.get("property_id"):
                property = await self.property_service.get_property(transaction_data["property_id"])
                if not property:
                    raise BadRequestException("Property not found")
                seller = await self.user_service.get_user_by_id(property.user_id)
                if not seller:
                    raise BadRequestException("Seller not found")
                transaction_data["seller_id"] = property.user_id
                users = await self.user_service.get_all_users()
                if not users:
                    raise BadRequestException("No users found")
                seller_location_id = await self.user_profile_service.get_user_profile_by_user_id(seller.id)
                seller_location = await self.location_service.get_location_by_id(seller_location_id.location_id)
                property_location = await self.location_service.get_location_by_id(property.location_id)
                eligible_notaries = []
                for user in users:
                    notary_profile = await self.user_profile_service.get_user_profile_by_user_id(str(user.id))
                    notary_location = await self.location_service.get_location_by_id(notary_profile.location_id)
                    if user.role == UserRole.NOTARY and notary_location.province\
                        == property_location.province == seller_location.province:
                        eligible_notaries.append(user.id)
                if len(eligible_notaries) > 0:
                    transaction_data["notary_id"] = random.choice(eligible_notaries)
                transaction_data["amount"] = property.price
            transaction = await self.transaction_repo.update_transaction(transaction_id, transaction_data)
            message = None
            if transaction_data.get("message"):
                if transaction_data.get("message"):
                    message = {
                        "content": transaction_data.pop("message"),
                    }            
                message["sender_id"] = transaction.buyer_id
                message["receiver_id"] = transaction.seller_id
                message["transaction_id"] = transaction.id
                message["property_id"] = transaction.property_id
                message["sent_at"] = datetime.now()
                await self.message_service.create_message(message)            
            else:
                transaction_data.pop("message")
            return transaction
        except BadRequestException as e:
            raise e
        except NotFoundException as e:
            raise e
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise InternalServerErrorException()
    
    async def get_transaction(self, transaction_id: str) -> Transaction:
        try:
            return await self.transaction_repo.get_transaction(transaction_id)
        except Exception as e:
            logger.error(f"Error getting transaction: {e}")
            raise InternalServerErrorException()
    
    async def delete_transaction(self, transaction_id: str) -> Transaction:
        try:
            return await self.transaction_repo.delete_transaction(transaction_id)
        except Exception as e:
            logger.error(f"Error deleting transaction: {e}")
            raise InternalServerErrorException()
    
    async def get_transactions(self) -> List[Transaction]:
        try:
            return await self.transaction_repo.get_transactions()
        except Exception as e:
            logger.error(f"Error get_transactions: {e}")
            raise InternalServerErrorException()
    
    async def get_transactions_by_buyer_id(self, user_id: str) -> List[Transaction]:
        try:
            return await self.transaction_repo.get_transactions_by_buyer_id(user_id)
        except Exception as e:
            logger.error(f"Error get_transactions_by_buyer_id: {e}")
            raise InternalServerErrorException()
    
    async def get_transactions_by_property(self, property_id: str) -> List[Transaction]:
        try:
            return await self.transaction_repo.get_transactions_by_property_id(property_id)
        except Exception as e:
            logger.error(f"Error get_transactions_by_property: {e}")
            raise InternalServerErrorException()
    
    async def get_transactions_by_status(self, status: str) -> List[Transaction]:
        try:
            if status:
                status_type = status.name
                status = getattr(TransactionStatus, status_type, None)
                if status is None:
                    raise BadRequestException(f"Invalid status: {status_type}")
            return await self.transaction_repo.get_transactions_by_status(status)
        except BadRequestException as e:
            raise e
        except Exception as e:
            logger.error(f"Error get_transactions_by_status: {e}")
            raise InternalServerErrorException()
    
    async def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        try:
            if transaction_type:
                transaction_type = transaction_type.name
                transaction = getattr(TransactionType, transaction_type, None)
                if transaction is None:
                    raise BadRequestException(f"Invalid Transaction type: {transaction}")
            return await self.transaction_repo.get_transactions_by_type(transaction)
        except BadRequestException as e:
            raise e
        except Exception as e:
            logger.error(f"Error getting transaction by type: {e}")
            raise InternalServerErrorException()
    
    async def get_transaction_by_transaction_number(self, transaction_number: str) -> Transaction:
        try:
            return await self.transaction_repo.get_transaction_by_transaction_number(transaction_number)
        except Exception as e:
            logger.error(f"Error getting transaction by transaction number: {e}")
            raise InternalServerErrorException()
    
    async def get_transaction_by_notary_id(self, notary_id: str) -> List[Transaction]:
        try:
            return await self.transaction_repo.get_transactions_by_notary_id(notary_id)
        except Exception as e:
            logger.error(f"Error getting transaction by notary id: {e}")
            raise InternalServerErrorException()
    
    async def get_transaction_by_seller_id(self, seller_id: str) -> List[Transaction]:
        try:
            return await self.transaction_repo.get_transactions_by_seller_id(seller_id)
        except Exception as e:
            logger.error(f"Error getting transaction by seller id: {e}")
            raise InternalServerErrorException()
        
    async def notary_approval(self, transaction_id: str, status: Enum) -> Transaction:
        try:
            if status:
                status_type = status.name
                status = getattr(TransactionStatus, status_type, None)
                if status is None:
                    raise BadRequestException(f"Invalid status: {status_type}")
            if not await self.transaction_repo.get_transaction(transaction_id):
                raise NotFoundException("Transaction not found")
            if status == TransactionStatus.ACCEPTED:
                transaction = await self.transaction_repo.update_transaction(transaction_id, {"status": status})
                await self.property_service.change_user_status(transaction.property_id, {
                    "user_id": transaction.buyer_id,
                    "status": PropertyStatus.SOLD
                    })
                return transaction
            elif status == TransactionStatus.DECLIEND:
                transaction = await self.transaction_repo.update_transaction(transaction_id, {"status": status})
                await self.property_service.change_user_status(transaction.property_id, {
                    "status": PropertyStatus.SELLING_CANCELLED
                    })
                return transaction
        except BadRequestException as e:
            raise e
        except NotFoundException as e:
            raise e
        except Exception as e:
            logger.error(f"Error updating transaction: {e}")
            raise InternalServerErrorException()
        