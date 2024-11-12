# main.py

from src.RestAPI.Auth import login, token
import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.middleware.CustomErrorHandler import CustomException, custom_exception_handler
from src.graphql.index import Query, Mutation
from src.startups.dbConn import startDBConnection

def init_app():
    app = FastAPI()
    startDBConnection(app)
        
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

    return app

app = init_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)