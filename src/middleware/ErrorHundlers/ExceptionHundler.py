from functools import wraps
from pydantic import ValidationError
from .CustomErrorHandler import (
    BadRequestException,
    NotFoundException,
    InternalServerErrorException,
    UnauthorizedException,
    ForbiddenException,
    GenericException,
)

class ExceptionHandler:
    @staticmethod
    def handle_exceptions(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except BadRequestException as e:
                raise e
            except NotFoundException as e:
                raise e
            except UnauthorizedException as e:
                raise e
            except ForbiddenException as e:
                raise e
            except GenericException as e:
                raise e
            except ValueError as e:
                raise e
            except TypeError as e:
                raise e
            except ValidationError as e:
                raise e
            except InternalServerErrorException as e:
                raise e
        return wrapper