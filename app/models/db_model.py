from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base


class EndPointCall(Base):
    __tablename__ = "endpoint_calls"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    call_latency = Column(Float)
