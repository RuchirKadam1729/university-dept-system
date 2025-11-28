from sqlalchemy import Column, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from typing import List, Optional
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    
    roll_number = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    admission_date = Column(Date, nullable=False)
    cgpa = Column(Float, default=0.0)
    
    # Relationships
    course_registrations = relationship("CourseRegistration", back_populates="student", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    grade_sheets = relationship("GradeSheet", back_populates="student", cascade="all, delete-orphan")
    
    def calculate_cgpa(self) -> float:
        """Calculate CGPA from all grades"""
        if not self.grades:
            return 0.0
        
        total_points = 0.0
        total_credits = 0
        
        for grade in self.grades:
            if grade.course and grade.is_pass():
                grade_points = grade.get_grade_points()
                credits = grade.course.credits
                total_points += grade_points * credits
                total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 2)
    
    def has_completed_course(self, course_id: str) -> bool:
        """Check if student has completed a specific course"""
        for registration in self.course_registrations:
            if registration.course_id == course_id and registration.completed:
                return True
        return False
    
    def get_backlog_courses(self) -> List['CourseRegistration']:
        """Get list of backlog courses"""
        return [reg for reg in self.course_registrations if reg.is_backlog()]