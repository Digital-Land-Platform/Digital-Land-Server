import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.config import Config
from src.models.Base import BaseModel

load_dotenv()

DB_CONFIG_is_defined = False

DB_CONFIG = Config.get_env_variable("DB_CONFIG")

if not DB_CONFIG: 
    # Database configuration
    DEV_DB_HOST = Config.get_env_variable("DEV_DB_HOST")
    DEV_DB_PORT = Config.get_env_variable("DEV_DB_PORT")
    DEV_DB_USER = Config.get_env_variable("DEV_DB_USER")
    DEV_DB_PASS = Config.get_env_variable("DEV_DB_PASS")
    DEV_DB_NAME = Config.get_env_variable("DEV_DB_NAME")

    if DEV_DB_HOST \
            and DEV_DB_PORT \
                and DEV_DB_USER \
                    and DEV_DB_PASS \
                        and DEV_DB_NAME:
         DB_CONFIG = f"postgresql+asyncpg://{DEV_DB_USER}:{DEV_DB_PASS}@{DEV_DB_HOST}:{DEV_DB_PORT}/{DEV_DB_NAME}"

    else:
        raise ValueError('Database variables are not defined in .env file.')
else:
    DB_CONFIG_is_defined = True
    
isDev = Config.get_env_variable("ENV_APP") == "dev"

print("==================================================>")
print("Initializing database...")
print("==================================================>")
if isDev:
    print(f"DB_CONFIG: {DB_CONFIG}")
else:
    if DB_CONFIG_is_defined:
        print(f"DB_CONFIG: Has been provided!")
    else:
        print(f"DB_CONFIG: Hasn't been provided!")
print("==================================================>")

class DatabaseSession:
    def __init__(self, url: str = DB_CONFIG):
        self.engine = create_async_engine(url, echo=isDev)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    # Generating models into a database
    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)

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