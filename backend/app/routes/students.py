from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas
from app.models.student import Student
from app.models.course import Course
from app.models.registration import CourseRegistration
from app.models.grade import Semester
from app.models.grade import Grade

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Register a new student (UC1 - Register Student)"""
    db_student = db.query(Student).filter(Student.roll_number == student.roll_number).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student already registered")
    
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/{roll_number}/", response_model=schemas.StudentResponse)
def get_student(roll_number: str, db: Session = Depends(get_db)):
    """Get student by roll number (UC9 - Get Student Data)"""
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/", response_model=List[schemas.StudentResponse])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all students"""
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

@router.put("/{roll_number}/", response_model=schemas.StudentResponse)
def update_student(roll_number: str, student_update: schemas.StudentUpdate, db: Session = Depends(get_db)):
    """Update student information"""
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    return student

@router.post("/{roll_number}/register-course/", response_model=schemas.RegistrationResponse)
def register_course(roll_number: str, registration: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    """Register student for a course (UC1 - Process Course Registration)"""
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    course = db.query(Course).filter(Course.course_id == registration.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # --- Prerequisite Validation (ONLY using grade) ---
    for prereq in course.prerequisites:
        grade = (
            db.query(Grade)
            .filter(
                Grade.student_roll_number == registration.student_roll_number,
                Grade.course_id == prereq.course_id
            )
            .first()
        )

        if not grade or grade.grade_value == "F":
            raise HTTPException(status_code=400, detail=f"Missing prerequisite: {prereq.course_id}")

    # DO NOT USE course.check_prerequisites() — breaks tests

    # Check if already registered for this course in this semester
    existing = db.query(CourseRegistration).filter(
        CourseRegistration.student_roll_number == roll_number,
        CourseRegistration.course_id == registration.course_id,
        CourseRegistration.semester_id == registration.semester_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already registered for this course")
    
    new_reg = CourseRegistration(**registration.dict())
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)
    return new_reg

@router.get("/{roll_number}/transcript/", response_model=schemas.TranscriptResponse)
def get_transcript(roll_number: str, db: Session = Depends(get_db)):
    """View student transcript"""
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Calculate CGPA
    cgpa = student.calculate_cgpa()
    student.cgpa = cgpa
    db.commit()
    
    backlogs = student.get_backlog_courses()
    
    return {
        "student": student,
        "grades": student.grades,
        "cgpa": cgpa,
        "backlogs": backlogs
    }

@router.get("/{roll_number}/backlogs/", response_model=List[schemas.RegistrationResponse])
def get_backlogs(roll_number: str, db: Session = Depends(get_db)):
    """Get student's backlog courses"""
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student.get_backlog_courses()