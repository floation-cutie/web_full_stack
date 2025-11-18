from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ServiceRequest(Base):
    __tablename__ = "sr_info"

    id = Column(Integer, primary_key=True, index=True)
    psr_userid = Column(Integer, ForeignKey("buser_table.id", ondelete="RESTRICT"), nullable=False, index=True)
    ps_title = Column(String(255), nullable=False)
    ps_begindate = Column(DateTime, nullable=False)
    ps_enddate = Column(DateTime, nullable=False)
    file_list = Column(Text)
    ps_state = Column(Integer, default=0)
    ps_desc = Column(Text)
    stype_id = Column(Integer, ForeignKey("service_type.id", ondelete="RESTRICT"), nullable=False, index=True)
    cityID = Column(Integer, ForeignKey("city_info.id", ondelete="RESTRICT"), nullable=False)

    user = relationship("BUser", backref="service_requests")
    service_type = relationship("ServiceType")
    city = relationship("CityInfo")
