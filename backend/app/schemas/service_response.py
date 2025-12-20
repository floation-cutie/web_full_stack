from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ServiceResponseCreate(BaseModel):
    sr_id: int
    title: str
    desc: str
    file_list: str

class ServiceResponseUpdate(BaseModel):
    title: str | None = None
    desc: str | None = None
    file_list: str | None = None
    response_state: int | None = None

class ServiceResponseResponse(BaseModel):
    response_id: int
    response_userid: int
    sr_id: int
    title: str | None
    desc: str | None
    response_state: int
    response_date: datetime
    file_list: str | None
    # Additional fields for responder information
    responder_name: Optional[str] = None
    responder_phone: Optional[str] = None

    class Config:
        from_attributes = True
