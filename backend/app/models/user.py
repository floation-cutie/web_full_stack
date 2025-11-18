from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class BUser(Base):
    __tablename__ = "buser_table"

    id = Column(Integer, primary_key=True, index=True)
    uname = Column(String(255), unique=True, nullable=False, index=True)
    ctype = Column(String(255), nullable=False)
    idno = Column(String(255), unique=True, nullable=False)
    bname = Column(String(50), nullable=False)
    bpwd = Column(String(255), nullable=False)
    phoneNo = Column(String(20), unique=True, nullable=False)
    rdate = Column(DateTime, nullable=False, default=datetime.utcnow)
    udate = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    userlvl = Column(String(8), nullable=True)
    desc = Column(String(255), nullable=True)
