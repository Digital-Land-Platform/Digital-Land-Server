from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from strawberry.exceptions import GraphQLError
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class InternalServerErrorException(CustomException):
    def __init__(self, detail: str = "Something went wrong! Try again later"):
        super().__init__(status_code=500, detail=detail)

class NotFoundException(CustomException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)

class UnauthorizedException(CustomException):
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(CustomException):
    def __init__(self, detail: str = "Forbidden access"):
        super().__init__(status_code=403, detail=detail)

class BadRequestException(CustomException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)

class GenericException(CustomException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": [{"message": exc.detail}]},
    )

async def graphql_exception_handler(request: Request, exc: GraphQLError):
    if isinstance(exc.original_error, NotFoundException):
        return JSONResponse(
            status_code=404,
            content={"errors": [{"message": exc.original_error.detail}]},
        )
    elif isinstance(exc.original_error, InternalServerErrorException):
        return JSONResponse(
            status_code=500,
            content={"errors": [{"message": exc.original_error.detail}]},
        )
    elif isinstance(exc.original_error, UnauthorizedException):
        return JSONResponse(
            status_code=401,
            content={"errors": [{"message": exc.original_error.detail}]},
        )
    elif isinstance(exc.original_error, BadRequestException):
        return JSONResponse(
            status_code=400,
            content={"errors": [{"message": exc.original_error.detail}]},
        )
    elif isinstance(exc.original_error, ForbiddenException):
        return JSONResponse(
            status_code=403,
            content={"errors": [{"message": exc.original_error.errors()}]},
        )
    elif isinstance(exc.original_error, GenericException):
        return JSONResponse(
            status_code=exc.original_error.status_code,
            content={"errors": [{"message": exc.original_error.detail}]},
        )
    elif isinstance(exc.original_error, ValidationError):
        return JSONResponse(
            status_code=422,
            content={"errors": [{"message": exc.original_error.errors()}]},
        )
    elif isinstance(exc.original_error, SQLAlchemyError):
        return JSONResponse(
            status_code=500,
            content={"errors": [{"message": "Database error"}]},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"errors": [{"message": exc.detail}]},
        )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": [{"message": exc.detail}]},
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"errors": [{"message": exc.errors()}]},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code | 500,
        content={"errors": [{"message": exc.detail}]},
    )
