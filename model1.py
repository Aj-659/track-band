from database import Base
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'user_cr'
    id = Column(Integer, primary_key=True, index=True,unique=True, nullable=False)
    Imei_no = Column(Integer, unique=True, nullable=False)
    Username = Column(String(50), unique=True, nullable=False)
    Password = Column(String(50), nullable=False, unique=True)
