from pydantic import BaseModel

# building the base validation class for others
class EndPointCallBase(BaseModel):
    content: str
    call_latency: float
    length: float


class EndPointCallCreate(EndPointCallBase):
    pass


class EndPointCall(EndPointCallBase):
    id: int

    class config:
        from_attribute = True  # pydantic > 2 (else orm_mode)
