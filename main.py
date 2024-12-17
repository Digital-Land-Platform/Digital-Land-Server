# main.py
import os

from pydantic import ValidationError
from graphql import GraphQLError
from config.config import Config
from src.RestAPI.Auth import login, token
import strawberry
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from src.middleware.ErrorHundlers.CustomErrorHandler import (
    CustomException, custom_exception_handler, graphql_exception_handler,
    http_exception_handler, validation_exception_handler, generic_exception_handler
)
from src.graphql.index import Query, Mutation
from src.startups.dbConn import startDBConnection
from config.logging import setup_logger, logger
from src.seeders.seed_database import Seeder
from config.database import db
import asyncio

isDev = Config.get_env_variable("ENV_APP") == "dev"
isSeedSet = Config.get_env_variable("SEED_DB") == "True"

def init_app():
    app = FastAPI()
    startDBConnection(app)

    # Get CLIENT_URL from environment variables
    CLIENT_URL = Config.get_env_variable("CLIENT_URL")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[CLIENT_URL],  # Allow only the client URL
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )

    # Set up logging
    setup_logger()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.get("/error")
    def get_error():
        raise CustomException(status_code=400, detail="This is a custom error message")
    
    app.include_router(login.router)
    app.include_router(token.router)
    
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema, multipart_uploads_enabled=True)

    app.include_router(graphql_app, prefix="/graphql")

    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(GraphQLError, graphql_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

        # seed_database on deployed database
    if not isDev and isSeedSet:
        @app.on_event("startup")
        async def startup_event():
            await seed_database()
            
    return app

app = init_app()

async def seed_database():
    """
    Seeds the database with initial data when ENV_APP is not dev.

    This function initializes the Seeder class with the database session
    and calls the seed_database method to populate the database with initial data.
    It is intended to be run asynchronously.

    Usage:
        await seed_database()
    """   
    seeder = Seeder(db)
    await seeder.seed_database()

# if not isDev and isSeedSet:
#     asyncio.create_task(seed_database())

PORT = Config.get_env_variable("PORT")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
