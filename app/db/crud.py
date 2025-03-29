from sqlalchemy.orm import Session

from app.models.db_model import EndPointCall
from app.schemas.db_schema import EndPointCallCreate

def create_endpointcall(db: Session, data: EndPointCallCreate):
    endpointcall_instance = EndPointCall(**data.model_dump())
    db.add(endpointcall_instance)
    db.commit()
    db.refresh(endpointcall_instance)
    return endpointcall_instance

def get_endpointcalls(db: Session):
    return db.query(EndPointCall).all()