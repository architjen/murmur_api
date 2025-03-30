from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# defining autocommit and autoflush to exclusively commit CRUD operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# the instance we'd use to interact with DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
