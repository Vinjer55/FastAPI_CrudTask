from fastapi import APIRouter, HTTPException
from src.schemas.student import StudentCreateRequest, StudentCreateRequest, StudentResponse
from src.db import models
from src.db.database import engine, db_dependency

models.Base.metadata.create_all(bind=engine)

student_router = APIRouter(
    tags=["Students"])

@student_router.get("/students", summary="Get all students")
async def get_students(db: db_dependency):
    
    try: 
        student_list = db.query(models.Students).order_by(models.Students.roll_no).all()
        return student_list
    except:
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@student_router.post("/students", summary="Create a new student")
async def create_student(student: StudentCreateRequest, db: db_dependency):
    db_student = models.Students(
            name=student.name,
            age=student.age,
            grade=student.grade
        )

    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        return {"message": "Student created successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@student_router.get("/students/{roll_no}", summary="Get a student by roll number")
async def get_student_by_roll_no(roll_no: int, db: db_dependency):
    student = db.query(models.Students).filter(models.Students.roll_no == roll_no).first()
    
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student

@student_router.put("/students/{roll_no}", summary="Update a student by roll number")
async def update_student(roll_no: int, student: StudentCreateRequest, db: db_dependency):
    db_student = db.query(models.Students).filter(models.Students.roll_no == roll_no).first()
    
    if db_student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        
    try:
        if student.name is not None:
            db_student.name = student.name
        if student.age is not None:
            db_student.age = student.age
        if student.grade is not None:
            db_student.grade = student.grade

        db.commit()
        db.refresh(db_student)
        
        return {"message": "Student updated successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@student_router.delete("/students/{roll_no}", summary="Delete a student by roll number")
async def delete_student(roll_no: int, db: db_dependency):
    db_student = db.query(models.Students).filter(models.Students.roll_no == roll_no).first()

    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        db.delete(db_student)
        db.commit()
        return {"message": "Student deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An internal error occurred.")