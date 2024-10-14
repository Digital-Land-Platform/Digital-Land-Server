# database.py

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel, Session
from typing import AsyncGenerator

load_dotenv()

# Load DB credentials from .env or throw an error if not set
DB_CONFIG = os.getenv("DB_CONFIG")

# Modified DB connection logic as the first one was bound to throw an error even when the .env file was set
def show_db_works():    
    """
    Print a message when database is being initialized.

    This function prints out a message with the database configuration
    string when the database is being initialized. This is useful for
    debugging purposes as it shows the database configuration string
    being used.

    """
    
    print("==================================================>")
    print("Initializing database...")
    print("==================================================>")
    print(f"DB_CONFIG: {DB_CONFIG}")
    print("==================================================>")

if DB_CONFIG:
    # Show that the DB is being initialized
    show_db_works()
    
elif not DB_CONFIG:  
    # Only load these other ones if DB_CONFIG is not set - takes care of redundancy  
    DEV_DB_HOST = os.getenv("DEV_DB_HOST")
    DEV_DB_PORT = os.getenv("DEV_DB_PORT")
    DEV_DB_USER = os.getenv("DEV_DB_USER")
    DEV_DB_PASS = os.getenv("DEV_DB_PASS")
    DEV_DB_NAME = os.getenv("DEV_DB_NAME")

    DB_CONFIG = f"postgresql+asyncpg://{DEV_DB_USER}:{DEV_DB_PASS}@{DEV_DB_HOST}:{DEV_DB_PORT}/{DEV_DB_NAME}"

    # Show that the DB is being initialized
    show_db_works()

else:
    # Throw an error if DB_CONFIG is not set both ways above
    raise ValueError('Database variables are not defined in .env file.')

# Class to manage database sessions
class DatabaseSession:
    def __init__(self, url: str = DB_CONFIG):
        self.engine = create_async_engine(url, echo=True)

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def close(self):
        await self.engine.dispose()

    # Context manager to automatically manage session lifecycle (enter/exit)
    async def __aenter__(self) -> Session:
        self.session = Session(self.engine)
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    # Dependency function for FastAPI to get the database session
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSession(self.engine) as session:
            yield session

    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

# Initialize the DB session globally
db = DatabaseSession()




# import os
# from dotenv import load_dotenv
# from typing import AsyncGenerator
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.sql import text
# from sqlmodel import SQLModel, Session

# load_dotenv()

# DB_CONFIG = os.getenv("DB_CONFIG")

# if not DB_CONFIG:
#     DEV_DB_HOST = os.getenv("DEV_DB_HOST")
#     DEV_DB_PORT = os.getenv("DEV_DB_PORT")
#     DEV_DB_USER = os.getenv("DEV_DB_USER")
#     DEV_DB_PASS = os.getenv("DEV_DB_PASS")
#     DEV_DB_NAME = os.getenv("DEV_DB_NAME")

#     DB_CONFIG = f"postgresql+asyncpg://{DEV_DB_USER}:{DEV_DB_PASS}@{DEV_DB_HOST}:{DEV_DB_PORT}/{DEV_DB_NAME}"
# else:
#     raise ValueError('Database variables are not defined in .env file.')

# print("==================================================>")
# print("Initializing database...")
# print("==================================================>")
# print(f"DB_CONFIG: {DB_CONFIG}")
# print("==================================================>")

# class DatabaseSession:
#     def __init__(self, url: str = DB_CONFIG):
#         self.engine = create_async_engine(url, echo=True)
#         self.SessionLocal = sessionmaker(
#             bind=self.engine,
#             class_=AsyncSession,
#             expire_on_commit=False,
#         )

#     # Generating models into a database
#     async def create_all(self):
#         async with self.engine.begin() as conn:
#             await conn.run_sync(SQLModel.metadata.create_all)

#     async def drop_all(self):
#         async with self.engine.begin() as conn:
#             await conn.run_sync(SQLModel.metadata.drop_all)

#     # close connection
#     async def close(self):
#         await self.engine.dispose()

#     # Prepare the context for the asynchronous operation
#     async def __aenter__(self) -> AsyncSession:
#         self.session = self.SessionLocal()
#         return self.session

#     # it is used to clean up resources,etc.
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         await self.session.close()

    # async def get_db(self) -> AsyncSession:
    #     async with self as db:
    #         yield db

#     async def commit_rollback(self):
#         try:
#             await self.session.commit()
#         except Exception:
#             await self.session.rollback()
#             raise


# db = DatabaseSession()
