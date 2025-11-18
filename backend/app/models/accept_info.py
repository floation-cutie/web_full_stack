from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class AcceptInfo(Base):
    __tablename__ = "accept_info"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("response_info.id", ondelete="RESTRICT"), nullable=False, index=True)
    accept_date = Column(DateTime, default=datetime.utcnow)

    response = relationship("ServiceResponse", backref="accept_info")
