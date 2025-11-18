from pydantic import BaseModel
from datetime import datetime

class ServiceRequestCreate(BaseModel):
    ps_title: str
    ps_begindate: datetime
    ps_enddate: datetime
    ps_desc: str | None = None
    stype_id: int
    cityID: int
    file_list: str | None = None

class ServiceRequestUpdate(BaseModel):
    ps_title: str | None = None
    ps_begindate: datetime | None = None
    ps_enddate: datetime | None = None
    ps_desc: str | None = None
    stype_id: int | None = None
    cityID: int | None = None
    file_list: str | None = None
    ps_state: int | None = None

class ServiceRequestResponse(BaseModel):
    id: int
    psr_userid: int
    ps_title: str
    ps_begindate: datetime
    ps_enddate: datetime
    ps_desc: str | None
    stype_id: int
    cityID: int
    file_list: str | None
    ps_state: int

    class Config:
        from_attributes = True
