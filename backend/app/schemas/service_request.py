from pydantic import BaseModel, Field
from datetime import datetime

class ServiceRequestCreate(BaseModel):
    sr_title: str = Field(..., min_length=1, max_length=80, description="Service request title")
    stype_id: int = Field(..., description="Service type ID")
    cityID: int = Field(..., description="City ID")
    desc: str = Field(..., min_length=1, max_length=300, description="Service description")
    file_list: str = Field("", max_length=300, description="Comma-separated file list")
    ps_begindate: datetime = Field(..., description="Start/publish date")

class ServiceRequestUpdate(BaseModel):
    sr_title: str | None = Field(None, min_length=1, max_length=80, description="Service request title")
    stype_id: int | None = Field(None, description="Service type ID")
    cityID: int | None = Field(None, description="City ID")
    desc: str | None = Field(None, min_length=1, max_length=300, description="Service description")
    file_list: str | None = Field(None, max_length=300, description="Comma-separated file list")
    ps_begindate: datetime | None = Field(None, description="Start/publish date")
    ps_state: int | None = Field(None, description="Service state: 0=published, -1=cancelled")
    ps_updatedate: datetime | None = Field(None, description="Update date")

class ServiceRequestResponse(BaseModel):
    sr_id: int
    sr_title: str
    stype_id: int
    psr_userid: int
    cityID: int
    desc: str
    file_list: str
    ps_begindate: datetime
    ps_state: int
    ps_updatedate: datetime | None = None

    class Config:
        from_attributes = True
