from sqlalchemy import Column, Integer, String
from app.database import Base


class CityInfo(Base):
    __tablename__ = "city_info"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(50), nullable=False)
    province = Column(String(50))
