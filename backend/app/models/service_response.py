from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ServiceResponse(Base):
    __tablename__ = "response_info"

    response_id = Column(Integer, primary_key=True, index=True)
    response_userid = Column(Integer, ForeignKey("buser_table.id", ondelete="RESTRICT"), nullable=False, index=True)
    sr_id = Column(Integer, ForeignKey("sr_info.sr_id", ondelete="RESTRICT"), nullable=False, index=True)
    response_desc = Column(Text)
    response_state = Column(Integer, default=0)
    response_date = Column(DateTime, default=datetime.utcnow)
    file_list = Column(Text)

    user = relationship("BUser", backref="service_responses")
    service_request = relationship("ServiceRequest", backref="responses")
