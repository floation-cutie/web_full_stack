from pydantic import BaseModel, Field
from datetime import datetime

class UserBase(BaseModel):
    uname: str
    bname: str
    ctype: str
    idno: str
    phoneNo: str
    desc: str | None = None
    cityID: int | None = None
    address: str | None = None

class UserResponse(UserBase):
    id: int
    rdate: datetime
    udate: datetime | None = None
    userlvl: str | None = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    bname: str | None = None
    phoneNo: str | None = Field(None, pattern=r"^1[3-9]\d{9}$")
    desc: str | None = None
    cityID: int | None = None
    address: str | None = None

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=100)
