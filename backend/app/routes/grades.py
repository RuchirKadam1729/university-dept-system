from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas
from app.models.grade import Grade, GradeSheet, Semester
from app.models.student import Student
from app.models.course import Course

router = APIRouter(prefix="/grades", tags=["grades"])

VALID_GRADES = {"A+", "A", "B+", "B", "C+", "C", "D", "F"}

@router.post("/", response_model=schemas.GradeResponse)
def enter_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    """Enter grade for a student (UC2 - Enter Grades)"""
    if grade.grade_value not in VALID_GRADES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid grade value. Must be one of: {', '.join(sorted(VALID_GRADES))}"
        )
    # Validate student exists
    student = (
        db.query(Student)
        .filter(Student.roll_number == grade.student_roll_number)
        .first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Validate course exists
    course = db.query(Course).filter(Course.course_id == grade.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Validate semester exists
    semester = (
        db.query(Semester).filter(Semester.semester_id == grade.semester_id).first()
    )
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")

    # Check if grade already exists
    existing_grade = (
        db.query(Grade)
        .filter(
            Grade.student_roll_number == grade.student_roll_number,
            Grade.course_id == grade.course_id,
            Grade.semester_id == grade.semester_id,
        )
        .first()
    )

    if existing_grade:
        # Update existing grade
        existing_grade.grade_value = grade.grade_value
        db.commit()
        db.refresh(existing_grade)
        return existing_grade

    # Create new grade
    new_grade = Grade(**grade.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)

    # Update student CGPA
    student.cgpa = student.calculate_cgpa()
    db.commit()

    return new_grade


@router.get("/student/{roll_number}/", response_model=List[schemas.GradeResponse])
def get_student_grades(
    roll_number: str, semester_id: str = None, db: Session = Depends(get_db)
):
    """Get grades for a student (UC3 - Get Grades)"""
    query = db.query(Grade).filter(Grade.student_roll_number == roll_number)

    if semester_id:
        query = query.filter(Grade.semester_id == semester_id)

    grades = query.all()
    if not grades:
        raise HTTPException(status_code=404, detail="No grades found")

    return grades


@router.get("/course/{course_id}/", response_model=List[schemas.GradeResponse])
def get_course_grades(
    course_id: str, semester_id: str = None, db: Session = Depends(get_db)
):
    """Get all grades for a course"""
    query = db.query(Grade).filter(Grade.course_id == course_id)

    if semester_id:
        query = query.filter(Grade.semester_id == semester_id)

    grades = query.all()
    return grades


@router.post("/gradesheet/generate/", response_model=schemas.GradeSheetResponse)
def generate_gradesheet(
    payload: schemas.GradeSheetCreate,
    db: Session = Depends(get_db)
):
    student_roll_number = payload.student_roll_number
    semester_id = payload.semester_id

    """Generate grade sheet for a student for a semester"""
    student = (
        db.query(Student).filter(Student.roll_number == student_roll_number).first()
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if gradesheet already exists
    existing_sheet = (
        db.query(GradeSheet)
        .filter(
            GradeSheet.student_roll_number == student_roll_number,
            GradeSheet.semester_id == semester_id,
        )
        .first()
    )

    if existing_sheet:
        # Recalculate GPA
        existing_sheet.gpa = existing_sheet.calculate_gpa()
        db.commit()
        db.refresh(existing_sheet)
        return existing_sheet

    # Create new gradesheet
    new_sheet = GradeSheet(
        student_roll_number=student_roll_number, semester_id=semester_id
    )
    db.add(new_sheet)
    db.commit()
    db.refresh(new_sheet)

    # Calculate GPA
    new_sheet.gpa = new_sheet.calculate_gpa()
    db.commit()
    db.refresh(new_sheet)

    return new_sheet


@router.get(
    "/gradesheet/{student_roll_number}/", response_model=List[schemas.GradeSheetResponse]
)
def get_gradesheets(student_roll_number: str, db: Session = Depends(get_db)):
    """Get all grade sheets for a student"""
    sheets = (
        db.query(GradeSheet)
        .filter(GradeSheet.student_roll_number == student_roll_number)
        .all()
    )
    return sheets
