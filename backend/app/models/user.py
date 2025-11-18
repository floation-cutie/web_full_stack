from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class BUser(Base):
    __tablename__ = "buser_table"

    id = Column(Integer, primary_key=True, index=True)
    uname = Column(String(50), unique=True, nullable=False, index=True)
    ctype = Column(String(50), nullable=False)
    idno = Column(String(50), unique=True, nullable=False)
    bname = Column(String(50), nullable=False)
    bpwd = Column(String(255), nullable=False)
    phoneNo = Column(String(11), unique=True, nullable=False)
    desc = Column(Text)
    psrDate = Column(DateTime, default=datetime.utcnow)
