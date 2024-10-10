from fastapi import APIRouter, HTTPException
from src.schemas.students import StudentCreateRequest, StudentCreateRequest, StudentResponse

user_router = APIRouter()

# Incrementing roll no.
current_roll_no = 1000

# In memory database
students_list = []

@user_router.get("/students")
def get_students():
    return students_list

@user_router.post("/students", response_model=StudentResponse)
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

@user_router.get("/students/{roll_no}")
def get_student_by_roll_no(roll_no: int):
    for student in students_list:
        if student.roll_no == roll_no:
            return student
    raise HTTPException(status_code=404, detail="Item not found")

@user_router.put("/students/{roll_no}", response_model=StudentResponse)
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

@user_router.delete("/students/{roll_no}")
def delete_student(roll_no: int):
    for i, s in enumerate(students_list):
        if s.roll_no == roll_no:
            students_list.pop(i)
            return {"message": "The student has been deleted"}
    raise HTTPException(status_code=404, detail="Item not found")