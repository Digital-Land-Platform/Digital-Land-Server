from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException, CustomException, InternalServerErrorException
)
from src.models.repository.AvailabilityRepository import AvailabilityRepository
from src.models.Availability import Availability
from src.models.enums.AvailabityStatus import AvailabilityStatus
from sqlalchemy.ext.asyncio import AsyncSession
from src.middleware.UserProfileValidator import UserProfileValidator
from typing import List, Dict


class AvailabilityService:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.availability_repo = AvailabilityRepository(db)
    
    async def create_availability(self, availability_data: Dict) -> Availability:
        try:
            if "status" in availability_data and availability_data.get("status"):
                status = availability_data.get("status").name
                availability_data["status"] = getattr(AvailabilityStatus, status, None)
                if availability_data["status"] is None:
                    raise BadRequestException("Invalid status")
            else:
                availability_data["status"] = AvailabilityStatus.AVAILABLE
            if "start_time" in availability_data and availability_data.get("start_time"):
                availability_data["start_time"] = UserProfileValidator.change_str_date(availability_data["start_time"])
            if "end_time" in availability_data and availability_data.get("end_time"):
                availability_data["end_time"] = UserProfileValidator.change_str_date(availability_data["end_time"])
            if not availability_data.get("start_time") or not availability_data.get("end_time"):
                raise BadRequestException("Start time and end time are required")
            check = await self.availability_repo.check_start_end_date(availability_data.get("natory_id"),
                                                                      availability_data.get("start_time"),
                                                                      availability_data.get("end_time"))
            if check is not None and len(check) > 0:
                raise CustomException(status_code=409, detail="You already provide for this time")
            new_availability = Availability(**availability_data)
            return await self.availability_repo.create_availability(new_availability)
        except BadRequestException as e:
            raise e
        except CustomException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def update_availability(self, availability_id: str, availability_data: Dict) -> Availability:
        try:
            if "status" in availability_data and availability_data.get("status"):
                availability_data["status"] = AvailabilityStatus[availability_data["status"]]
            if "start_time" in availability_data and availability_data.get("start_time"):
                availability_data["start_time"] = UserProfileValidator.change_str_date(availability_data["start_time"])
            if "end_time" in availability_data and availability_data.get("end_time"):
                availability_data["end_time"] = UserProfileValidator.change_str_date(availability_data["end_time"])
            return await self.availability_repo.update_availability(availability_id, availability_data)
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_availability(self, availability_id: str) -> Availability:
        try:
            if not availability_id:
                raise BadRequestException("Availability ID is required.")
            return await self.availability_repo.get_availability(availability_id)
        except BadRequestException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def delete_availability(self, availability_id: str) -> str:
        try:
            if not availability_id:
                raise BadRequestException("Availability ID is required.")
            return await self.availability_repo.delete_availability(availability_id)
        except BadRequestException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    async def get_availability_by_status(self, status: str) -> List[Availability]:
        try:
            if not status:
                raise BadRequestException("Availability status is required.")
            status = AvailabilityStatus[status.status.name]
            return await self.availability_repo.get_availability_by_status(status)
        except BadRequestException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()
    
    
    async def get_all_availability(self) -> List[Availability]:
        try:
            return await self.availability_repo.get_all_availability()
        except Exception as e:
            raise InternalServerErrorException()