# main.py

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.middleware.CustomErrorHandler import CustomException, custom_exception_handler
from src.graphql.index import Query, Mutation

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/error")
def get_error():
    raise CustomException(status_code=400, detail="This is a custom error message")

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

app.add_exception_handler(CustomException, custom_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# def init_app():
#     app = FastAPI()

#     @app.get("/")
#     def read_root():
#         return {"Hello": "World"}

#     @app.get("/error")
#     def get_error():
#         raise CustomException(status_code=400, detail="This is a custom error message")

#     schema = strawberry.Schema(query=Query, mutation=Mutation)
#     graphql_app = GraphQLRouter(schema)

#     app.include_router(graphql_app, prefix="/graphql")

#     app.add_exception_handler(CustomException, custom_exception_handler)

#     return app

# if __name__ == "__main__":
#     import uvicorn
#     app = init_app()
#     uvicorn.run(app, host="0.0.0.0", port=8000)
