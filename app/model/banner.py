from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base

class Banner(Base):
    __tablename__ = "banner"
    
    id = Column(Integer, primary_key=True, comment="아이디")
    url = Column(String(255), nullable=False, comment="주소")
    
        
