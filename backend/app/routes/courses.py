from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas
from app.models.course import Course
from app.models.grade import Semester

router = APIRouter(tags=["courses"])

@router.post("/courses/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """Create a new course"""
    db_course = db.query(Course).filter(Course.course_id == course.course_id).first()
    if db_course:
        raise HTTPException(status_code=400, detail="Course already exists")
    
    new_course = Course(
        course_id=course.course_id,
        course_name=course.course_name,
        credits=course.credits
    )
    
    # Add prerequisites
    for prereq_id in course.prerequisite_ids:
        prereq = db.query(Course).filter(Course.course_id == prereq_id).first()
        if prereq:
            new_course.add_prerequisite(prereq)
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/courses/{course_id}/", response_model=schemas.CourseResponse)
def get_course(course_id: str, db: Session = Depends(get_db)):
    """Get course by ID"""
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/courses/", response_model=List[schemas.CourseResponse])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all courses"""
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.post("/semesters/", response_model=schemas.SemesterResponse)
def create_semester(semester: schemas.SemesterCreate, db: Session = Depends(get_db)):
    """Create a new semester"""
    db_semester = db.query(Semester).filter(Semester.semester_id == semester.semester_id).first()
    if db_semester:
        raise HTTPException(status_code=400, detail="Semester already exists")
    
    new_semester = Semester(**semester.dict())
    db.add(new_semester)
    db.commit()
    db.refresh(new_semester)
    return new_semester

@router.get("/semesters/", response_model=List[schemas.SemesterResponse])
def list_semesters(db: Session = Depends(get_db)):
    """List all semesters"""
    semesters = db.query(Semester).all()
    return semesters