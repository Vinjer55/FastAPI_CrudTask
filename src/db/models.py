from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from src.db.database import Base

class Students(Base):
    __tablename__ = "students"
    
    roll_no = Column(Integer, Sequence('roll_no_seq', start=1001, increment=1),
                 primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String, index=True)
    email = Column(String, index=True)
    is_active = Column(Integer)
    enrollment_date = Column(String, index=True)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    