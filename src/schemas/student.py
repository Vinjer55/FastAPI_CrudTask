from pydantic import BaseModel

class StudentBase(BaseModel):
    roll_no: int
    name: str
    age: int
    grade: str |  None = None
    email: str | None = None
    is_active: bool = True
    enrollment_date: str | None = None  
    
class StudentCreateRequest(BaseModel):
    name: str
    age: int
    grade: str |  None = None
    
class StudentResponse(BaseModel):
    roll_no: int
    name: str
    age: int
    grade: str |  None = None