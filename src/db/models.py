from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from db.database import Base

class User(Base):
    __tablename__ = "students"
    
    roll_no = Column(Integer, Sequence('roll_no_seq', start=1000, increment=1),
                 primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String, index=True)
    email = Column(String, index=True)
    is_active = Column(Integer)
    enrollment_date = Column(String, index=True)
    