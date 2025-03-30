from sqlalchemy import Column, Integer, String, Float

# custom import(s)
from app.db.database import Base

# defining schema model for our table endpoint_calls in database
class EndPointCall(Base):
    __tablename__ = "endpoint_calls"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    call_latency = Column(Float)
    length = Column(Float)
