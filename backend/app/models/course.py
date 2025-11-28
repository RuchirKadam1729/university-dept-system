from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from typing import List
from app.database import Base

# Association table for course prerequisites
course_prerequisites = Table(
    'course_prerequisites',
    Base.metadata,
    Column('course_id', String, ForeignKey('courses.course_id'), primary_key=True),
    Column('prerequisite_id', String, ForeignKey('courses.course_id'), primary_key=True)
)

class Course(Base):
    __tablename__ = "courses"
    
    course_id = Column(String, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    
    # Self-referential relationship for prerequisites
    prerequisites = relationship(
        "Course",
        secondary=course_prerequisites,
        primaryjoin=course_id == course_prerequisites.c.course_id,
        secondaryjoin=course_id == course_prerequisites.c.prerequisite_id,
        backref="required_for"
    )
    
    # Relationships
    registrations = relationship("CourseRegistration", back_populates="course")
    grades = relationship("Grade", back_populates="course")
    
    def check_prerequisites(self, student: 'Student') -> bool:
        """Check if student has completed all prerequisites"""
        for prereq in self.prerequisites:
            if not student.has_completed_course(prereq.course_id):
                return False
        return True
    
    def add_prerequisite(self, prerequisite: 'Course'):
        """Add a prerequisite course"""
        if prerequisite not in self.prerequisites:
            self.prerequisites.append(prerequisite)