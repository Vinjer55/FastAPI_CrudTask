from fastapi import APIRouter
from schemas.students import StudentCreateRequest, StudentCreateRequest, StudentResponse

user_router = APIRouter()

# Incrementing roll no.
current_roll_no = 1000

# In memory database
students_list = []

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