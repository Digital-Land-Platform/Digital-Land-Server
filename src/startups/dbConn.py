from fastapi import FastAPI

from config.database import DatabaseSession

db = DatabaseSession()

async def startup():
    try:
        await db.create_all()
        print("==================================================>")
        print("Database connected successfully")
        print("==================================================>")
    except Exception as e:
        print("==================================================>")
        print(f"Failed to connect to database: {str(e)}")
        print("==================================================>")
        raise e

async def shutdown():
    try:
        await db.close()
        print("==================================================>")
        print("Database connection closed successfully")
        print("==================================================>")
    except Exception as e:
        print("==================================================>")
        print(f"Failed to close database connection: {str(e)}")
        print("==================================================>")
        raise e

def startDBConnection(apps: FastAPI):
    apps.lifespan_context = {"startup": startup, "shutdown": shutdown}

app = FastAPI()
startDBConnection(app)

# def startDBConnection(apps: FastAPI):
#     @apps.on_event("startup")
#     async def startup():
#         try:
#             await db.create_all()
#             print("==================================================>")
#             print("Database connected successfully")
#             print("==================================================>")
#         except Exception as e:
#             print("==================================================>")
#             print(f"Failed to connect to database: {str(e)}")
#             print("==================================================>")
#             raise e

#     @apps.on_event("shutdown")
#     async def shutdown():
#         try:
#             await db.close()
#             print("==================================================>")
#             print("Database connection closed successfully")
#             print("==================================================>")
#         except Exception as e:
#             print("==================================================>")
#             print(f"Failed to close database connection: {str(e)}")
#             print("==================================================>")
#             raise e
    