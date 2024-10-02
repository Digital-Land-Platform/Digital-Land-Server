import strawberry
import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from strawberry.fastapi import GraphQLRouter

from config.logging import setup_logger
# queries and mutations
from src.graphql.index import Mutation, Query
from src.middleware.CustomErrorHandler import (CustomException,
                                               custom_exception_handler,
                                               http_exception_handler)
from src.startups.dbConn import startDBConnection


def init_app():
    apps = FastAPI(title="Mobility Server", description="Fast API", version="1.0.0")

    # Start database connection
    startDBConnection(apps)

    @apps.get("/health")
    def health():
        return {"status": "OK"}, 200

    @apps.get("/")
    def home():
        return "welcome home!"

    @apps.get("/error")
    def get_error():
        raise CustomException(status_code=400, detail="This is a custom error message")

    # # Register GraphQL API
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)

    apps.include_router(graphql_app, prefix="/graphql")

    return apps


# Start the Service Manager
app = init_app()

# Set up logging
setup_logger()

# Register error handlers
app.exception_handler(CustomException)(custom_exception_handler)
app.exception_handler(StarletteHTTPException)(http_exception_handler)

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
