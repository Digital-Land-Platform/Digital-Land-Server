import asyncio
from config.database import db
from src.models import Property, User
from src.models.Base import Base

async def init_db():
    print("Creating tables...")
    
    async with db.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
