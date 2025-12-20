from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ServiceResponse(Base):
    __tablename__ = "response_info"

    response_id = Column(Integer, primary_key=True, index=True)
    response_userid = Column(Integer, ForeignKey("buser_table.id", ondelete="RESTRICT"), nullable=False, index=True)
    sr_id = Column(Integer, ForeignKey("sr_info.sr_id", ondelete="RESTRICT"), nullable=False, index=True)
    title = Column(String(50), nullable=False)
    desc = Column(String(500), nullable=False)
    response_state = Column(Integer, default=0)
    response_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, nullable=True)
    file_list = Column(String(400), nullable=False)

    user = relationship("BUser", backref="service_responses")
    service_request = relationship("ServiceRequest", backref="responses")
