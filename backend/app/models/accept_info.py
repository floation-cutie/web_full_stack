from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class AcceptInfo(Base):
    __tablename__ = "accept_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    srid = Column(Integer, ForeignKey("sr_info.sr_id", ondelete="RESTRICT"), nullable=False, index=True)
    psr_userid = Column(Integer, ForeignKey("buser_table.id", ondelete="RESTRICT"), nullable=False)
    response_id = Column(Integer, ForeignKey("response_info.response_id", ondelete="RESTRICT"), nullable=False, index=True)
    response_userid = Column(Integer, ForeignKey("buser_table.id", ondelete="RESTRICT"), nullable=False)
    createdate = Column(DateTime, nullable=False, default=datetime.utcnow)
    desc = Column(Integer, nullable=True)

    response = relationship("ServiceResponse", foreign_keys=[response_id], backref="accept_info")
    service_request = relationship("ServiceRequest", foreign_keys=[srid])
    publisher = relationship("BUser", foreign_keys=[psr_userid])
    responder = relationship("BUser", foreign_keys=[response_userid])
