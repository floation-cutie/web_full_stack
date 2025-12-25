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
    cityID = Column(Integer, nullable=True)
    address = Column(String(255), nullable=True)
    
    @property
    def service_requests_count(self):
        # Return the count of service requests published by this user
        return len(self.service_requests) if hasattr(self, 'service_requests') else 0
    
    @property
    def service_responses_count(self):
        # Return the count of service responses made by this user
        return len(self.service_responses) if hasattr(self, 'service_responses') else 0
    
    @property
    def completed_services_count(self):
        # Return the count of completed services (accepted responses)
        if not hasattr(self, 'service_responses'):
            return 0
            
        count = 0
        for response in self.service_responses:
            if response.response_state == 1:  # Accepted state
                count += 1
        return count
