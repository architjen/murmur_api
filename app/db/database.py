from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)

# defining autocommit and autoflush to exclusively commit CRUD operations
AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    class_=AsyncSession
    )

Base = declarative_base()

# the instance we'd use to interact with DB
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

