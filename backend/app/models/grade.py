from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from typing import List

class Semester(Base):
    __tablename__ = "semesters"
    
    semester_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)  # e.g., "Fall 2024"
    year = Column(Integer, nullable=False)
    
    # Relationships
    grades = relationship("Grade", back_populates="semester")
    grade_sheets = relationship("GradeSheet", back_populates="semester")
    registrations = relationship("CourseRegistration", back_populates="semester")

class Grade(Base):
    __tablename__ = "grades"
    
    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    student_roll_number = Column(String, ForeignKey("students.roll_number"), nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    grade_value = Column(String, nullable=False)  # A, B, C, D, F
    semester_id = Column(String, ForeignKey("semesters.semester_id"), nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    semester = relationship("Semester", back_populates="grades")
    
    def get_grade_points(self) -> float:
        """Convert letter grade to grade points"""
        grade_map = {
            'A': 10.0, 'A+': 10.0,
            'B': 8.0, 'B+': 9.0,
            'C': 6.0, 'C+': 7.0,
            'D': 5.0,
            'F': 0.0
        }
        return grade_map.get(self.grade_value.upper(), 0.0)
    
    def is_pass(self) -> bool:
        """Check if grade is passing"""
        return self.grade_value.upper() != 'F'

class GradeSheet(Base):
    __tablename__ = "grade_sheets"
    
    sheet_id = Column(Integer, primary_key=True, autoincrement=True)
    student_roll_number = Column(String, ForeignKey("students.roll_number"), nullable=False)
    semester_id = Column(String, ForeignKey("semesters.semester_id"), nullable=False)
    gpa = Column(Float, default=0.0)
    
    # Relationships
    student = relationship("Student", back_populates="grade_sheets")
    semester = relationship("Semester", back_populates="grade_sheets")
    
    def calculate_gpa(self) -> float:
        """Calculate GPA for this semester"""
        semester_grades = [g for g in self.student.grades if g.semester_id == self.semester_id]
        
        if not semester_grades:
            return 0.0
        
        total_points = 0.0
        total_credits = 0
        
        for grade in semester_grades:
            if grade.course:
                grade_points = grade.get_grade_points()
                credits = grade.course.credits
                total_points += grade_points * credits
                total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 2)