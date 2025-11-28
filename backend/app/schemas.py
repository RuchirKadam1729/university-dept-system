from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# Student Schemas
class StudentBase(BaseModel):
    roll_number: str
    name: str
    address: Optional[str] = None
    admission_date: date

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

class StudentResponse(StudentBase):
    cgpa: float
    
    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    course_id: str
    course_name: str
    credits: int

class CourseCreate(CourseBase):
    prerequisite_ids: Optional[List[str]] = []

class CourseResponse(CourseBase):
    prerequisites: List['CourseResponse'] = []
    
    class Config:
        from_attributes = True

# Grade Schemas
class GradeBase(BaseModel):
    student_roll_number: str
    course_id: str
    grade_value: str
    semester_id: str

class GradeCreate(GradeBase):
    pass

class GradeSheetCreate(BaseModel):
    student_roll_number: str
    semester_id: str
    
class GradeResponse(GradeBase):
    grade_id: int
    
    class Config:
        from_attributes = True

# GradeSheet Schemas
class GradeSheetResponse(BaseModel):
    sheet_id: int
    student_roll_number: str
    semester_id: str
    gpa: float
    
    class Config:
        from_attributes = True

# CourseRegistration Schemas
class RegistrationCreate(BaseModel):
    student_roll_number: str
    course_id: str
    semester_id: str

class RegistrationResponse(BaseModel):
    registration_id: int
    student_roll_number: str
    course_id: str
    semester_id: str
    registration_date: date
    completed: bool
    
    class Config:
        from_attributes = True

# Semester Schema
class SemesterBase(BaseModel):
    semester_id: str
    name: str
    year: int

class SemesterCreate(SemesterBase):
    pass

class SemesterResponse(SemesterBase):
    class Config:
        from_attributes = True

# Transcript Schema
class TranscriptResponse(BaseModel):
    student: StudentResponse
    grades: List[GradeResponse]
    cgpa: float
    backlogs: List[RegistrationResponse]