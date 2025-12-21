from sqlalchemy import Column, Integer, String
from app.database import Base


class CityInfo(Base):
    __tablename__ = "city_info"

    cityID = Column(Integer, primary_key=True, index=True)
    cityName = Column(String(255))
    provinceID = Column(Integer)
    provinceName = Column(String(255))
