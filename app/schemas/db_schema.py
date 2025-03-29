from pydantic import BaseModel

class EndPointCallBase(BaseModel):
    content: str
    call_latency: float
    

class EndPointCallCreate(EndPointCallBase):
    pass

class EndPointCall(EndPointCallBase):
    id: int
    class config:
        from_attribute = True # pydantic > 2 (else orm_mode)