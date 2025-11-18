from pydantic import BaseModel, Field, field_validator

class UserRegister(BaseModel):
    uname: str = Field(..., min_length=3, max_length=50)
    ctype: str = Field(..., description="ID type")
    idno: str = Field(..., min_length=6, max_length=50)
    bname: str = Field(..., min_length=2, max_length=50)
    bpwd: str = Field(..., min_length=6, max_length=100)
    phoneNo: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    desc: str | None = None

    @field_validator("bpwd")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")

        digit_count = sum(c.isdigit() for c in v)
        if digit_count < 2:
            raise ValueError("Password must contain at least 2 digits")

        if v.isupper() or v.islower():
            raise ValueError("Password cannot be all uppercase or all lowercase")

        return v

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
    user_info: dict
