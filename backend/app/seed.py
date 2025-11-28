#usage: at project root, run: docker compose exec backend python -m app.seed
from datetime import date
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.models.student import Student
from app.models.course import Course
from app.models.grade import Grade
from app.models.grade import Semester
from app.models.registration import CourseRegistration

print("Running SEED SCRIPT...")

Base.metadata.create_all(bind=engine)

session = Session(bind=engine)

# ---------------------------------------------------------------------
# SEMESTERS (Create these first)
# ---------------------------------------------------------------------
semesters = [
    Semester(semester_id="FALL2023", name="Fall 2023", year=2023),
    Semester(semester_id="SPRING2024", name="Spring 2024", year=2024),
    Semester(semester_id="FALL2024", name="Fall 2024", year=2024),
    Semester(semester_id="SPRING2025", name="Spring 2025", year=2025),
]

for sem in semesters:
    if not session.get(Semester, sem.semester_id):
        session.add(sem)

session.commit()

# ---------------------------------------------------------------------
# COURSES (Comprehensive Computer Science Curriculum)
# ---------------------------------------------------------------------
courses = [
    # First Year - Semester 1
    Course(course_id="CS101", course_name="Introduction to Programming", credits=4),
    Course(course_id="MATH101", course_name="Calculus I", credits=3),
    Course(course_id="PHYS101", course_name="Physics I", credits=3),
    Course(course_id="ENG101", course_name="English Composition", credits=3),
    
    # First Year - Semester 2
    Course(course_id="CS102", course_name="Object-Oriented Programming", credits=4),
    Course(course_id="MATH102", course_name="Calculus II", credits=3),
    Course(course_id="PHYS102", course_name="Physics II", credits=3),
    Course(course_id="CHEM101", course_name="Chemistry", credits=3),
    
    # Second Year - Semester 1
    Course(course_id="CS201", course_name="Data Structures", credits=4),
    Course(course_id="CS202", course_name="Computer Architecture", credits=4),
    Course(course_id="MATH201", course_name="Discrete Mathematics", credits=3),
    Course(course_id="STAT101", course_name="Statistics", credits=3),
    
    # Second Year - Semester 2
    Course(course_id="CS203", course_name="Algorithms", credits=4),
    Course(course_id="CS204", course_name="Database Systems", credits=4),
    Course(course_id="CS205", course_name="Operating Systems", credits=4),
    Course(course_id="MATH202", course_name="Linear Algebra", credits=3),
    
    # Third Year - Semester 1
    Course(course_id="CS301", course_name="Software Engineering", credits=4),
    Course(course_id="CS302", course_name="Computer Networks", credits=4),
    Course(course_id="CS303", course_name="Web Development", credits=3),
    Course(course_id="CS304", course_name="Machine Learning", credits=4),
    
    # Third Year - Semester 2
    Course(course_id="CS305", course_name="Artificial Intelligence", credits=4),
    Course(course_id="CS306", course_name="Cloud Computing", credits=3),
    Course(course_id="CS307", course_name="Cybersecurity", credits=4),
    Course(course_id="CS308", course_name="Mobile App Development", credits=3),
    
    # Fourth Year - Electives
    Course(course_id="CS401", course_name="Deep Learning", credits=4),
    Course(course_id="CS402", course_name="Blockchain Technology", credits=3),
    Course(course_id="CS403", course_name="Computer Vision", credits=4),
    Course(course_id="CS404", course_name="Natural Language Processing", credits=4),
    Course(course_id="CS405", course_name="DevOps and CI/CD", credits=3),
]

for c in courses:
    if not session.get(Course, c.course_id):
        session.add(c)

session.commit()

# Add prerequisites (must be done after all courses exist)
prereq_map = {
    "CS102": ["CS101"],  # OOP requires Intro to Programming
    "CS201": ["CS102"],  # Data Structures requires OOP
    "CS203": ["CS201"],  # Algorithms requires Data Structures
    "CS204": ["CS201"],  # Database requires Data Structures
    "CS205": ["CS202"],  # OS requires Computer Architecture
    "CS301": ["CS203"],  # Software Eng requires Algorithms
    "CS304": ["CS203", "MATH201"],  # ML requires Algorithms & Discrete Math
    "CS305": ["CS304"],  # AI requires ML
    "CS401": ["CS304"],  # Deep Learning requires ML
}

for course_id, prereq_ids in prereq_map.items():
    course = session.get(Course, course_id)
    if course:
        for prereq_id in prereq_ids:
            prereq = session.get(Course, prereq_id)
            if prereq and prereq not in course.prerequisites:
                course.prerequisites.append(prereq)

session.commit()

# ---------------------------------------------------------------------
# STUDENTS (Diverse batch)
# ---------------------------------------------------------------------
students = [
    # Year 4 (2021 batch) - Senior students
    Student(roll_number="2021001", name="Rajesh Kumar", address="Mumbai", admission_date=date(2021, 8, 1)),
    Student(roll_number="2021002", name="Priya Patel", address="Ahmedabad", admission_date=date(2021, 8, 1)),
    Student(roll_number="2021003", name="Arjun Singh", address="Delhi", admission_date=date(2021, 8, 1)),
    
    # Year 3 (2022 batch) - Junior students
    Student(roll_number="2022001", name="Sneha Reddy", address="Hyderabad", admission_date=date(2022, 8, 1)),
    Student(roll_number="2022002", name="Vikram Malhotra", address="Bangalore", admission_date=date(2022, 8, 1)),
    Student(roll_number="2022003", name="Aisha Khan", address="Pune", admission_date=date(2022, 8, 1)),
    
    # Year 2 (2023 batch) - Sophomore students
    Student(roll_number="2023001", name="Rahul Sharma", address="Chennai", admission_date=date(2023, 8, 1)),
    Student(roll_number="2023002", name="Ananya Iyer", address="Mumbai", admission_date=date(2023, 8, 1)),
    Student(roll_number="2023003", name="Karthik Nair", address="Kochi", admission_date=date(2023, 8, 1)),
    
    # Year 1 (2024 batch) - Freshmen
    Student(roll_number="2024001", name="Meera Desai", address="Surat", admission_date=date(2024, 8, 1)),
    Student(roll_number="2024002", name="Rohan Verma", address="Jaipur", admission_date=date(2024, 8, 1)),
    Student(roll_number="2024003", name="Tanvi Shah", address="Kolkata", admission_date=date(2024, 8, 1)),
]

for s in students:
    if not session.get(Student, s.roll_number):
        session.add(s)

session.commit()

# ---------------------------------------------------------------------
# COURSE REGISTRATIONS & GRADES
# ---------------------------------------------------------------------

# Year 2 Student (2023001) - Excellent student, progressing normally
registrations_2023001 = [
    # Fall 2023 (1st semester - completed)
    ("2023001", "CS101", "FALL2023", True, "A+"),
    ("2023001", "MATH101", "FALL2023", True, "A"),
    ("2023001", "PHYS101", "FALL2023", True, "B+"),
    ("2023001", "ENG101", "FALL2023", True, "A"),
    
    # Spring 2024 (2nd semester - completed)
    ("2023001", "CS102", "SPRING2024", True, "A"),
    ("2023001", "MATH102", "SPRING2024", True, "B+"),
    ("2023001", "PHYS102", "SPRING2024", True, "B"),
    ("2023001", "CHEM101", "SPRING2024", True, "A"),
    
    # Fall 2024 (3rd semester - in progress, some grades available)
    ("2023001", "CS201", "FALL2024", False, "A"),
    ("2023001", "CS202", "FALL2024", False, "A+"),
    ("2023001", "MATH201", "FALL2024", False, None),
    ("2023001", "STAT101", "FALL2024", False, None),
]

# Year 2 Student (2023002) - Average student
registrations_2023002 = [
    # Fall 2023
    ("2023002", "CS101", "FALL2023", True, "B+"),
    ("2023002", "MATH101", "FALL2023", True, "B"),
    ("2023002", "PHYS101", "FALL2023", True, "C+"),
    ("2023002", "ENG101", "FALL2023", True, "B"),
    
    # Spring 2024
    ("2023002", "CS102", "SPRING2024", True, "B"),
    ("2023002", "MATH102", "SPRING2024", True, "C+"),
    ("2023002", "PHYS102", "SPRING2024", True, "B+"),
    ("2023002", "CHEM101", "SPRING2024", True, "B"),
    
    # Fall 2024
    ("2023002", "CS201", "FALL2024", False, "B+"),
    ("2023002", "CS202", "FALL2024", False, None),
    ("2023002", "MATH201", "FALL2024", False, None),
]

# Year 3 Student (2022001) - Has a backlog
registrations_2022001 = [
    # Fall 2023
    ("2022001", "CS101", "FALL2023", True, "A"),
    ("2022001", "MATH101", "FALL2023", True, "B"),
    ("2022001", "PHYS101", "FALL2023", True, "F"),  # Failed - backlog!
    ("2022001", "ENG101", "FALL2023", True, "B+"),
    
    # Spring 2024
    ("2022001", "CS102", "SPRING2024", True, "A"),
    ("2022001", "MATH102", "SPRING2024", True, "B"),
    ("2022001", "CHEM101", "SPRING2024", True, "C+"),
    
    # Fall 2024 (repeating failed course + new courses)
    ("2022001", "PHYS101", "FALL2024", False, "B+"),  # Retaking - now passing!
    ("2022001", "CS201", "FALL2024", False, "A"),
    ("2022001", "CS202", "FALL2024", False, "B+"),
]

# Year 3 Student (2022002) - Strong student
registrations_2022002 = [
    # Fall 2023
    ("2022002", "CS101", "FALL2023", True, "A+"),
    ("2022002", "MATH101", "FALL2023", True, "A"),
    ("2022002", "PHYS101", "FALL2023", True, "A"),
    ("2022002", "ENG101", "FALL2023", True, "A+"),
    
    # Spring 2024
    ("2022002", "CS102", "SPRING2024", True, "A+"),
    ("2022002", "MATH102", "SPRING2024", True, "A"),
    ("2022002", "PHYS102", "SPRING2024", True, "A"),
    ("2022002", "CHEM101", "SPRING2024", True, "A"),
    
    # Fall 2024
    ("2022002", "CS201", "FALL2024", True, "A+"),
    ("2022002", "CS202", "FALL2024", True, "A"),
    ("2022002", "MATH201", "FALL2024", True, "A+"),
    ("2022002", "STAT101", "FALL2024", False, "A"),
]

# Year 4 Student (2021001) - Senior, almost graduated
registrations_2021001 = [
    # Previous semesters (Fall 2023 & Spring 2024 - showing recent ones)
    ("2021001", "CS301", "FALL2023", True, "A"),
    ("2021001", "CS302", "FALL2023", True, "B+"),
    ("2021001", "CS303", "FALL2023", True, "A"),
    ("2021001", "CS304", "FALL2023", True, "B+"),
    
    # Spring 2024
    ("2021001", "CS305", "SPRING2024", True, "A"),
    ("2021001", "CS306", "SPRING2024", True, "B+"),
    ("2021001", "CS307", "SPRING2024", True, "A+"),
    
    # Fall 2024 - Final semester electives
    ("2021001", "CS401", "FALL2024", False, "A"),
    ("2021001", "CS402", "FALL2024", False, "B+"),
]

# Fresh student (2024001) - Just started, no grades yet
registrations_2024001 = [
    # Fall 2024 (1st semester - in progress, no grades)
    ("2024001", "CS101", "FALL2024", False, None),
    ("2024001", "MATH101", "FALL2024", False, None),
    ("2024001", "PHYS101", "FALL2024", False, None),
    ("2024001", "ENG101", "FALL2024", False, None),
]

# Fresh student (2024002) - Started getting some grades
registrations_2024002 = [
    # Fall 2024 (1st semester - some early grades)
    ("2024002", "CS101", "FALL2024", False, "A"),
    ("2024002", "MATH101", "FALL2024", False, "B+"),
    ("2024002", "PHYS101", "FALL2024", False, None),
    ("2024002", "ENG101", "FALL2024", False, None),
]

# Struggling student (2024003) - Not doing well
registrations_2024003 = [
    # Fall 2024
    ("2024003", "CS101", "FALL2024", False, "C"),
    ("2024003", "MATH101", "FALL2024", False, "D"),
    ("2024003", "PHYS101", "FALL2024", False, "C+"),
    ("2024003", "ENG101", "FALL2024", False, None),
]

# Combine all registrations
all_registrations = (
    registrations_2023001 + 
    registrations_2023002 +
    registrations_2022001 + 
    registrations_2022002 +
    registrations_2021001 +
    registrations_2024001 +
    registrations_2024002 +
    registrations_2024003
)

for student_roll, course_id, semester_id, completed, grade_value in all_registrations:
    # Check if registration exists
    exists_reg = (
        session.query(CourseRegistration)
        .filter_by(
            student_roll_number=student_roll,
            course_id=course_id,
            semester_id=semester_id,
        )
        .first()
    )
    
    if not exists_reg:
        reg = CourseRegistration(
            student_roll_number=student_roll,
            course_id=course_id,
            semester_id=semester_id,
            completed=completed,
        )
        session.add(reg)
    
    # Add grade if provided
    if grade_value:
        exists_grade = (
            session.query(Grade)
            .filter_by(
                student_roll_number=student_roll,
                course_id=course_id,
                semester_id=semester_id,
            )
            .first()
        )
        
        if not exists_grade:
            grade = Grade(
                student_roll_number=student_roll,
                course_id=course_id,
                grade_value=grade_value,
                semester_id=semester_id,
            )
            session.add(grade)

session.commit()

# Update CGPA for all students
for student in session.query(Student).all():
    student.cgpa = student.calculate_cgpa()

session.commit()

print("✅ Database seeding complete!")
print("\n📊 Summary:")
print(f"   - {len(semesters)} semesters created")
print(f"   - {len(courses)} courses created")
print(f"   - {len(students)} students registered")
print("\n🎓 Sample Students (test these!):")
print("   • 2024001 - Fresh student, no grades yet")
print("   • 2024002 - Fresh student, getting A's and B's")
print("   • 2024003 - Struggling student (C's and D's)")
print("   • 2023001 - 2nd year, excellent student (A's)")
print("   • 2023002 - 2nd year, average student (B's and C's)")
print("   • 2022001 - 3rd year, HAS BACKLOG in PHYS101 (retaking)")
print("   • 2022002 - 3rd year, outstanding student (all A's)")
print("   • 2021001 - 4th year senior, almost graduated")
print("\n📚 Course IDs available:")
print("   1st Year: CS101, CS102, MATH101-102, PHYS101-102, ENG101, CHEM101")
print("   2nd Year: CS201-205 (Data Structures, Algorithms, etc.)")
print("   3rd Year: CS301-308 (Software Eng, ML, AI, etc.)")
print("   4th Year: CS401-405 (Deep Learning, Blockchain, etc.)")
print("\n📅 Semesters: FALL2023, SPRING2024, FALL2024, SPRING2025")
print("\n💡 Quick tests:")
print("   - View transcript for 2022001 to see the BACKLOG")
print("   - Compare CGPAs: 2022002 (highest) vs 2024003 (lowest)")
print("   - Register 2024001 for a course (they have none yet)")