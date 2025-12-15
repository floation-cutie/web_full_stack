from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ServiceRequest(Base):
    __tablename__ = "sr_info"

    sr_id = Column(Integer, primary_key=True, index=True)
    sr_title = Column(String(80), nullable=False)
    stype_id = Column(Integer, ForeignKey("service_type.id", ondelete="RESTRICT"), nullable=False, index=True)
    psr_userid = Column(Integer, ForeignKey("buser_table.id", ondelete="RESTRICT"), nullable=False, index=True)
    cityID = Column(Integer, ForeignKey("city_info.id", ondelete="RESTRICT"), nullable=False)
    desc = Column(String(300), nullable=False)
    file_list = Column(String(300), nullable=False)
    ps_begindate = Column(DateTime, nullable=False)
    ps_state = Column(Integer, default=0, nullable=False)
    ps_updatedate = Column(DateTime, nullable=True)

    user = relationship("BUser", backref="service_requests")
    service_type = relationship("ServiceType")
    city = relationship("CityInfo")
