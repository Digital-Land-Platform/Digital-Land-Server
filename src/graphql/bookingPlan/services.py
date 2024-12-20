from src.middleware.ErrorHundlers.CustomErrorHandler import (
    BadRequestException, CustomException, InternalServerErrorException, NotFoundException
)
from src.models.BookingPlan import BookingPlan
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List
from src.models.repository.BookingPlanRepository import BookingPlanRepository
from src.models.enums.BookingPlanStatus import BookingPlanStatus
from src.middleware.UserProfileValidator import UserProfileValidator
from src.graphql.availability.services import AvailabilityService
from src.graphql.transaction.services import TransactionService

class BookingPlanService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.booking_plan_repo = BookingPlanRepository(db)
        self.availability_service = AvailabilityService(db)
        self.transaction_service = TransactionService(db)

    async def create_booking_plan(self, booking_plan_data: Dict) -> BookingPlan:
        try:
            if "status" in booking_plan_data and booking_plan_data.get("status"):
                status = booking_plan_data.get("status").name
                booking_plan_data["status"] = getattr(BookingPlanStatus, status, None)
                if booking_plan_data["status"] is None:
                    raise BadRequestException(detail="Invalid status")
            else:
                booking_plan_data["status"] = BookingPlanStatus.BOOKED

            availability = await self.availability_service.get_availability(booking_plan_data.get("availability_id"))
            if not availability:
                raise NotFoundException(detail="Availability not found")

            if "start_time" in booking_plan_data and booking_plan_data.get("start_time"):
                booking_plan_data["start_time"] = UserProfileValidator.change_str_date(booking_plan_data["start_time"])
            else:
                booking_plan_data["start_time"] = availability.start_time

            if "end_time" in booking_plan_data and booking_plan_data.get("end_time"):
                booking_plan_data["end_time"] = UserProfileValidator.change_str_date(booking_plan_data["end_time"])
            else:
                booking_plan_data["end_time"] = availability.end_time

            if not booking_plan_data.get("natory_id"):
                booking_plan_data["natory_id"] = availability.natory_id

            if not booking_plan_data.get("start_time") or not booking_plan_data.get("end_time"):
                raise BadRequestException(detail="Start time and end time are required")

            if not await self.transaction_service.get_transaction(booking_plan_data.get("transaction_id")):
                raise NotFoundException(detail="Invalid transaction ID")

            check = await self.booking_plan_repo.check_start_end_date(
                booking_plan_data.get("natory_id"),
                booking_plan_data.get("transaction_id"),
                booking_plan_data.get("start_time"),
                booking_plan_data.get("end_time")
            )

            if check is not None and len(check) > 0:
                raise CustomException(status_code=409, detail="You already provide for this time")

            new_booking_plan = BookingPlan(**booking_plan_data)
            return await self.booking_plan_repo.create_booking_plan(new_booking_plan)
        except (BadRequestException, NotFoundException, CustomException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def update_booking_plan(self, booking_plan_id: str, booking_plan_data: Dict) -> BookingPlan:
        try:
            if "status" in booking_plan_data and booking_plan_data.get("status"):
                status = booking_plan_data.get("status").name
                booking_plan_data["status"] = getattr(BookingPlanStatus, status, None)

            availability = None
            if "availability_id" in booking_plan_data and booking_plan_data.get("availability_id"):
                availability = await self.availability_service.get_availability(booking_plan_data.get("availability_id"))
                if not availability:
                    raise NotFoundException(detail="Availability not found")

            if "start_time" in booking_plan_data and booking_plan_data.get("start_time"):
                booking_plan_data["start_time"] = UserProfileValidator.change_str_date(booking_plan_data["start_time"])
            elif availability:
                booking_plan_data["start_time"] = availability.start_time

            if "end_time" in booking_plan_data and booking_plan_data.get("end_time"):
                booking_plan_data["end_time"] = UserProfileValidator.change_str_date(booking_plan_data["end_time"])
            elif availability:
                booking_plan_data["end_time"] = availability.end_time

            if "transaction_id" in booking_plan_data and booking_plan_data.get("transaction_id"):
                if not await self.transaction_service.get_transaction(booking_plan_data.get("transaction_id")):
                    raise NotFoundException(detail="Invalid transaction ID")

            return await self.booking_plan_repo.update_booking_plan(booking_plan_id, booking_plan_data)
        except (BadRequestException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def get_booking_plan(self, booking_plan_id: str) -> BookingPlan:
        try:
            booking_plan = await self.booking_plan_repo.get_booking_plan(booking_plan_id)
            if not booking_plan:
                raise NotFoundException(detail="Booking plan not found")
            return booking_plan
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def delete_booking_plan(self, booking_plan_id: str) -> str:
        try:
            result = await self.booking_plan_repo.delete_booking_plan(booking_plan_id)
            if not result:
                raise NotFoundException(detail="Booking plan not found")
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()

    async def get_all_booking_plan(self) -> List[BookingPlan]:
        try:
            return await self.booking_plan_repo.get_all_booking_plan()
        except Exception as e:
            raise InternalServerErrorException()

    async def get_booking_plan_by_status(self, status: str) -> List[BookingPlan]:
        try:
            if status:
                status = getattr(BookingPlanStatus, status, None)
                if not status:
                    raise BadRequestException(detail="Invalid status")
            return await self.booking_plan_repo.get_booking_plan_by_status(status)
        except (BadRequestException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException()