import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlmodel import SQLModel

load_dotenv()

DB_CONFIG = os.getenv("DB_CONFIG")

# Database configuration
DEV_DB_HOST = os.getenv("DEV_DB_HOST", "localhost")
DEV_DB_PORT = os.getenv("DEV_DB_PORT", "5432")
DEV_DB_USER = os.getenv("DEV_DB_USER", "test_user")
DEV_DB_PASS = os.getenv("DEV_DB_PASS", "test_pass")
DEV_DB_NAME = os.getenv("DEV_DB_NAME", "test_db")

if not DB_CONFIG:
    if DEV_DB_HOST \
            and DEV_DB_PORT \
                and DEV_DB_USER \
                    and DEV_DB_PASS \
                        and DEV_DB_NAME:
         DB_CONFIG = f"postgresql+asyncpg://{DEV_DB_USER}:{DEV_DB_PASS}@{DEV_DB_HOST}:{DEV_DB_PORT}/{DEV_DB_NAME}"

    else:
        raise ValueError('Database variables are not defined in .env file.')

print("==================================================>")
print("Initializing database...")
print("==================================================>")
print(f"DB_CONFIG: {DB_CONFIG}")
print("==================================================>")

class DatabaseSession:
    def __init__(self, url: str = DB_CONFIG):
        self.engine = create_async_engine(url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    # Generating models into a database
    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    # close connection
    async def close(self):
        await self.engine.dispose()

    # Prepare the context for the asynchronous operation
    async def __aenter__(self) -> AsyncSession:
        self.session = self.SessionLocal()
        return self.session

    # it is used to clean up resources,etc.
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_db(self) -> AsyncSession:
        async with self as db:
            yield db

    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise


db = DatabaseSession()
