from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# custom import(s)
from app.models.db_model import EndPointCall
from app.schemas.db_schema import EndPointCallCreate


# function to insert transcription and other to DB
async def create_endpointcall(db: AsyncSession, data: EndPointCallCreate):
    endpointcall_instance = EndPointCall(**data.model_dump())
    db.add(endpointcall_instance)  # no async to add objects in DB
    await db.commit()
    await db.refresh(endpointcall_instance)
    return endpointcall_instance


# function to read from DB
async def get_endpointcalls(db: AsyncSession):
    result = await db.execute(select(EndPointCall))
    all_data = result.scalars().all()
    return all_data
