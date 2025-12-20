from sqlalchemy import Column, Integer, String
from app.database import Base


class ServiceType(Base):
    __tablename__ = "service_type"

    id = Column(Integer, primary_key=True, index=True)
    typename = Column(String(50), nullable=False)
    # service_desc doesn't exist in the database schema
