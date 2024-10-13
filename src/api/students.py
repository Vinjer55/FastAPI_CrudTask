from fastapi import APIRouter, HTTPException
from schemas.student import StudentCreateRequest, StudentCreateRequest, StudentResponse

student_router = APIRouter(
    tags=["Students"])

# Incrementing roll no.
current_roll_no = 1000

# In memory database
students_list = []

@student_router.get("/students", summary="Get all students")
def get_students():
    return students_list

@student_router.post("/students", response_model=StudentResponse, summary="Create a new student")
def create_student(student: StudentCreateRequest):
    global current_roll_no
    current_roll_no += 1
    
    try:
        new_student = StudentResponse(
            roll_no = current_roll_no,
            name = student.name,
            age = student.age, 
            grade = student.grade)

        students_list.append(new_student)
        return new_student
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@student_router.get("/students/{roll_no}", summary="Get a student by roll number")
def get_student_by_roll_no(roll_no: int):
    
    try:
        for student in students_list:
            if student.roll_no == roll_no:
                return student
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@student_router.put("/students/{roll_no}", response_model=StudentResponse, summary="Update a student by roll number")
def update_student(roll_no: int, student: StudentCreateRequest):
    
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@student_router.delete("/students/{roll_no}", summary="Delete a student by roll number")
def delete_student(roll_no: int):
    
    try: 
        for i, s in enumerate(students_list):
            if s.roll_no == roll_no:
                students_list.pop(i)
                return {"message": "The student has been deleted"}
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))