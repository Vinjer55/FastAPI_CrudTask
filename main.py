from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Incrementing roll no.
current_roll_no = 1000

# In memory database
students_list = []

class StudentBase(BaseModel):
    email: str | None = None
    is_active: bool = True
    enrollment_date: str | None = None

class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str |  None = None
    
class StudentResponse(StudentCreate):
    roll_no: int
    
@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate):
    global current_roll_no
    current_roll_no += 1
    
    new_student = StudentResponse(
        roll_no = current_roll_no,
        name = student.name,
        age = student.age, 
        grade = student.grade)

    students_list.append(new_student)
    return new_student

@app.get("/students")
def get_students():
    return students_list

@app.get("/students/{roll_no}")
def get_student_by_roll_no(roll_no: int):
    for student in students_list:
        if student.roll_no == roll_no:
            return student
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/students/{roll_no}", response_model=StudentResponse)
def update_student(roll_no: int, student: StudentCreate):
    for i, s in enumerate(students_list):
        if s.roll_no == roll_no:
            updated_student = StudentResponse(
                roll_no=s.roll_no,
                name=student.name,
                age=student.age,
                grade=student.grade
            )
            students_list[i] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/students/{roll_no}")
def delete_student(roll_no: int):
    for i, s in enumerate(students_list):
        if s.roll_no == roll_no:
            students_list.pop(i)
            return {"message": "The student has been deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
