from typing import Annotated
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from .schemas.students import StudentCreateRequest, StudentCreateRequest, StudentResponse

app = FastAPI()

# Incrementing roll no.
current_roll_no = 1000

# In memory database
students_list = []
    
@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreateRequest):
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
def update_student(roll_no: int, student: StudentCreateRequest):
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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
    )
