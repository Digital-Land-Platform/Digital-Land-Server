from fastapi import FastAPI
import os
from config.database import DatabaseSession

db = DatabaseSession()


def startDBConnection(apps: FastAPI):
    if os.getenv("TESTING", "false") == "true":
        print("Skipping database initialization during testing")
        return
    @apps.on_event("startup")
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

    @apps.on_event("shutdown")
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