from sqlalchemy import Column, String, Date, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class CourseRegistration(Base):
    __tablename__ = "course_registrations"
    
    registration_id = Column(Integer, primary_key=True, autoincrement=True)
    student_roll_number = Column(String, ForeignKey("students.roll_number"), nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    semester_id = Column(String, ForeignKey("semesters.semester_id"), nullable=False)
    registration_date = Column(Date, default=date.today)
    completed = Column(Boolean, default=False)
    
    # Relationships
    student = relationship("Student", back_populates="course_registrations")
    course = relationship("Course", back_populates="registrations")
    semester = relationship("Semester", back_populates="registrations")
    
    def mark_completed(self):
        """Mark course as completed"""
        self.completed = True
    
    def is_backlog(self) -> bool:
        """Check if this is a backlog course"""
        # Check if student has a grade for this course
        for grade in self.student.grades:
            if grade.course_id == self.course_id and grade.semester_id == self.semester_id:
                return not grade.is_pass()
        
        # If registered but no grade, consider it incomplete (potential backlog)
        return not self.completed