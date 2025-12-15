from pydantic import BaseModel
from datetime import datetime

class ServiceResponseCreate(BaseModel):
    sr_id: int
    response_desc: str | None = None
    file_list: str | None = None

class ServiceResponseUpdate(BaseModel):
    response_desc: str | None = None
    file_list: str | None = None
    response_state: int | None = None

class ServiceResponseResponse(BaseModel):
    response_id: int
    response_userid: int
    sr_id: int
    response_desc: str | None
    response_state: int
    response_date: datetime
    file_list: str | None

    class Config:
        from_attributes = True
