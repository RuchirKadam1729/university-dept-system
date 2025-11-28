# University Department Information System
## Full-Stack Implementation

**Authors:** Ruchir Kadam (2023300098), Amruta Johare (2023300095)  
**Course:** Software Engineering  
**Instructor:** Prof. Prasenjit Bhavathankar

---

## Project Abstract

This project implements a complete full-stack University Department Information System based on our Software Requirements Specification (SRS), UML Use Case Diagrams, and Class Diagrams developed in previous experiments. The system automates administrative processes for university departments, including student management, course registration, and grade management.

### Implemented Modules

We have fully implemented **2 core modules** as required:

1. **Student Management Module** - Implements UC1 (Register Student), UC9 (Get Student Data), and course registration functionality
2. **Grade Management Module** - Implements UC2 (Enter Grades) and UC3 (Get Grades) with GPA calculation

---

## Architecture Overview

### Technology Stack

**Backend:**
- Python 3.11
- FastAPI (REST API framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)

**Frontend:**
- React 18 with TypeScript
- Vite (Build tool)
- Axios (HTTP client)
- React Router (Navigation)

**Deployment:**
- Docker & Docker Compose
- Cloudflare Tunnels (for public access)
- Nginx (Frontend web server)

### System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend  │────▶│   Backend    │────▶│  PostgreSQL  │
│   (React)   │     │  (FastAPI)   │     │   Database   │
└─────────────┘     └──────────────┘     └──────────────┘
       │                    │
       ▼                    ▼
┌─────────────┐     ┌──────────────┐
│  Cloudflare │     │  Cloudflare  │
│   Tunnel    │     │    Tunnel    │
└─────────────┘     └──────────────┘
```

---

## Class Diagram Implementation

The backend implementation strictly follows the class diagram from **Experiment 3**. Here's the mapping:

### Python Models → Java Classes

| Java Class (Experiment 3) | Python Model | File Location |
|---------------------------|--------------|---------------|
| `Student` | `Student` | `backend/app/models/student.py` |
| `Course` | `Course` | `backend/app/models/course.py` |
| `Grade` | `Grade` | `backend/app/models/grade.py` |
| `GradeSheet` | `GradeSheet` | `backend/app/models/grade.py` |
| `CourseRegistration` | `CourseRegistration` | `backend/app/models/registration.py` |
| `Semester` | `Semester` | `backend/app/models/grade.py` |

### Key Relationships Implemented

1. **Student ↔ CourseRegistration**: One-to-Many (A student can register for multiple courses)
2. **Student ↔ Grade**: One-to-Many (A student has multiple grades)
3. **Course ↔ Course**: Many-to-Many (Prerequisites relationship)
4. **Grade ↔ Course**: Many-to-One (Each grade is for one course)
5. **GradeSheet → Student**: Many-to-One (Multiple grade sheets per student)

### Class Methods Implemented

All key methods from the class diagram are implemented:

**Student class:**
- `calculate_cgpa()` - Calculates cumulative GPA
- `has_completed_course()` - Checks course completion
- `get_backlog_courses()` - Returns list of backlogs

**Course class:**
- `check_prerequisites()` - Validates prerequisites
- `add_prerequisite()` - Adds prerequisite course

**Grade class:**
- `get_grade_points()` - Converts letter grades to points
- `is_pass()` - Checks if grade is passing

**GradeSheet class:**
- `calculate_gpa()` - Calculates semester GPA

---

## Project Structure

```
university-dept-system/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── student.py           # Student entity
│   │   │   ├── course.py            # Course entity with prerequisites
│   │   │   ├── grade.py             # Grade, GradeSheet, Semester
│   │   │   └── registration.py      # CourseRegistration entity
│   │   ├── routes/
│   │   │   ├── students.py          # Student management endpoints
│   │   │   ├── grades.py            # Grade management endpoints
│   │   │   └── courses.py           # Course & semester endpoints
│   │   ├── database.py              # Database configuration
│   │   ├── schemas.py               # Pydantic validation schemas
│   │   └── main.py                  # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StudentManagement.tsx    # Student module UI
│   │   │   └── GradeManagement.tsx      # Grade module UI
│   │   ├── App.tsx                      # Main application
│   │   ├── App.css                      # Styles
│   │   └── main.tsx                     # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── nginx.conf
│   └── .env
└── docker-compose.yml
```

---

## Setup and Deployment

### Prerequisites

- Docker Desktop installed
- Docker Compose installed
- Git

### Installation Steps

1. **Clone or create the project directory:**
```bash
mkdir university-dept-system
cd university-dept-system
```

2. **Create environment files:**

**backend/.env:**
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/university_dept
```

**frontend/.env:**
```
VITE_API_URL=http://localhost:8000
```

3. **Deploy with Docker Compose:**
```bash
docker-compose up --build
```

This command will:
- Build the backend and frontend containers
- Start PostgreSQL database
- Initialize database tables
- Start Cloudflare tunnels for public access

### Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### Cloudflare Tunnels

The Docker Compose configuration includes Cloudflare tunnels that create public URLs. Check the logs to find your public URLs:

```bash
docker-compose logs backend-tunnel
docker-compose logs frontend-tunnel
```

Look for lines containing `https://` URLs.

---

## Module 1: Student Management

### Implemented Use Cases

**UC1 - Register Student:**
- Add new student with roll number, name, address, admission date
- Automatic CGPA initialization
- Duplicate prevention

**UC9 - Get Student Data:**
- View all students
- Search by roll number
- View complete student profile with CGPA

**Course Registration:**
- Register students for courses
- Prerequisite validation
- Duplicate registration prevention
- Semester-based registration

**View Transcript:**
- Complete academic record
- All grades with courses
- Calculated CGPA
- List of backlog courses

### API Endpoints

```
POST   /students/                          # Register new student
GET    /students/                          # List all students
GET    /students/{roll_number}             # Get student details
PUT    /students/{roll_number}             # Update student info
POST   /students/{roll_number}/register-course  # Register for course
GET    /students/{roll_number}/transcript  # View transcript
GET    /students/{roll_number}/backlogs    # Get backlogs
```

### Features

1. **Student Registration Form:**
   - Input: Roll Number, Name, Address, Admission Date
   - Validation: Required fields, unique roll number
   - Auto-calculation: CGPA initialized to 0.0

2. **Student List View:**
   - Grid display of all students
   - Shows name, roll number, and CGPA
   - Click to select student for operations

3. **Course Registration:**
   - Select student, course, and semester
   - Automatic prerequisite checking
   - Prevention of duplicate registrations

4. **Transcript View:**
   - Student details with current CGPA
   - Table of all grades by course and semester
   - List of backlog courses (failed or incomplete)

---

## Module 2: Grade Management

### Implemented Use Cases

**UC2 - Enter Grades:**
- Enter grades for students in courses
- Grade validation (A+, A, B+, B, C+, C, D, F)
- Update existing grades
- Automatic CGPA recalculation

**UC3 - Get Grades:**
- View grades by student
- Filter by semester
- View grades by course
- Display in tabular format

**Grade Sheet Generation:**
- Generate semester-wise grade sheets
- Calculate semester GPA
- Store grade sheet records

### API Endpoints

```
POST   /grades/                           # Enter/update grade
GET    /grades/student/{roll_number}      # Get student grades
GET    /grades/course/{course_id}         # Get course grades
POST   /grades/gradesheet/generate        # Generate grade sheet
GET    /grades/gradesheet/{roll_number}   # Get all grade sheets
```

### Features

1. **Grade Entry Form:**
   - Input: Student Roll Number, Course ID, Grade Value, Semester
   - Dropdown for grade selection (A+ to F)
   - Updates existing grades automatically
   - Real-time CGPA calculation

2. **Grade Query Interface:**
   - Search by student roll number
   - Optional semester filter
   - Displays grades in sortable table
   - Shows course ID, grade, and semester

3. **Grade Sheet Generation:**
   - Input: Student and Semester
   - Calculates semester GPA
   - Stores grade sheet record
   - Displays generated GPA

### Grade Point Calculation

The system uses the following grade-to-point mapping:

| Grade | Points |
|-------|--------|
| A+, A | 10.0   |
| B+    | 9.0    |
| B     | 8.0    |
| C+    | 7.0    |
| C     | 6.0    |
| D     | 5.0    |
| F     | 0.0    |

**CGPA Calculation:**
```
CGPA = Σ(Grade Points × Credits) / Σ(Credits)
```

---

## Database Schema

### Tables

1. **students**
   - roll_number (PK)
   - name
   - address
   - admission_date
   - cgpa

2. **courses**
   - course_id (PK)
   - course_name
   - credits

3. **course_prerequisites** (Junction table)
   - course_id (FK)
   - prerequisite_id (FK)

4. **semesters**
   - semester_id (PK)
   - name
   - year

5. **course_registrations**
   - registration_id (PK)
   - student_roll_number (FK)
   - course_id (FK)
   - semester_id (FK)
   - registration_date
   - completed

6. **grades**
   - grade_id (PK)
   - student_roll_number (FK)
   - course_id (FK)
   - semester_id (FK)
   - grade_value

7. **grade_sheets**
   - sheet_id (PK)
   - student_roll_number (FK)
   - semester_id (FK)
   - gpa

---

## Testing the System

### Sample Data Creation

1. **Create a Semester:**
```bash
curl -X POST http://localhost:8000/semesters \
  -H "Content-Type: application/json" \
  -d '{"semester_id": "SEM1", "name": "Fall 2024", "year": 2024}'
```

2. **Create Courses:**
```bash
curl -X POST http://localhost:8000/courses \
  -H "Content-Type: application/json" \
  -d '{"course_id": "CS101", "course_name": "Introduction to Programming", "credits": 4, "prerequisite_ids": []}'

curl -X POST http://localhost:8000/courses \
  -H "Content-Type: application/json" \
  -d '{"course_id": "CS201", "course_name": "Data Structures", "credits": 4, "prerequisite_ids": ["CS101"]}'
```

3. **Register Student:**
```bash
curl -X POST http://localhost:8000/students/ \
  -H "Content-Type: application/json" \
  -d '{"roll_number": "2023001", "name": "John Doe", "address": "123 Main St", "admission_date": "2023-08-01"}'
```

4. **Register Course:**
```bash
curl -X POST http://localhost:8000/students/2023001/register-course \
  -H "Content-Type: application/json" \
  -d '{"student_roll_number": "2023001", "course_id": "CS101", "semester_id": "SEM1"}'
```

5. **Enter Grade:**
```bash
curl -X POST http://localhost:8000/grades/ \
  -H "Content-Type: application/json" \
  -d '{"student_roll_number": "2023001", "course_id": "CS101", "grade_value": "A", "semester_id": "SEM1"}'
```

### Frontend Testing

1. Open http://localhost:3000
2. Navigate to **Students** tab
3. Fill the registration form and submit
4. Select a student from the list
5. Register the student for courses
6. View transcript to see CGPA and grades
7. Navigate to **Grades** tab
8. Enter grades for students
9. Query grades by student
10. Generate grade sheets

---

## Screenshots

*(Add screenshots here showing:)*

### 1. Student Registration
![Student Registration Form](screenshots/student-registration.png)
*Screenshot showing the student registration form with fields for roll number, name, address, and admission date*

### 2. Student List View
![Student List](screenshots/student-list.png)
*Screenshot showing the grid view of all registered students with their CGPA*

### 3. Course Registration
![Course Registration](screenshots/course-registration.png)
*Screenshot showing the course registration interface with prerequisite validation*

### 4. Student Transcript
![Transcript View](screenshots/transcript.png)
*Screenshot showing complete student transcript with grades, CGPA, and backlogs*

### 5. Grade Entry
![Grade Entry Form](screenshots/grade-entry.png)
*Screenshot showing the grade entry interface with dropdown for grade selection*

### 6. Grade Query Results
![Grade Query](screenshots/grade-query.png)
*Screenshot showing grades displayed in tabular format with filtering options*

### 7. Grade Sheet
![Grade Sheet](screenshots/grade-sheet.png)
*Screenshot showing generated grade sheet with semester GPA*

### 8. API Documentation
![API Docs](screenshots/api-docs.png)
*Screenshot of FastAPI automatic documentation at /docs endpoint*

---

## Key Features Demonstrated

### From Use Case Diagrams (Experiment 2)

✅ **UC1 - Register Student**: Complete CRUD operations for students  
✅ **UC2 - Enter Grades**: Grade entry with validation and CGPA calculation  
✅ **UC3 - Get Grades**: Query grades by student and semester  
✅ **UC9 - Get Student Data**: Retrieve student information and transcripts  

### From Class Diagram (Experiment 3)

✅ All entities implemented as SQLAlchemy models  
✅ All relationships (One-to-Many, Many-to-Many) implemented  
✅ All class methods from diagram implemented  
✅ Prerequisite checking and backlog detection  
✅ GPA and CGPA calculation algorithms  

### From SRS Document

✅ RESTful API architecture  
✅ Role-based access (foundation laid)  
✅ Data validation and error handling  
✅ PostgreSQL database with proper schema  
✅ Docker deployment  
✅ Cross-platform compatibility  

---

## Technical Highlights

### Backend

1. **FastAPI Framework:**
   - Automatic API documentation
   - Type validation with Pydantic
   - Async support for scalability
   - Built-in error handling

2. **SQLAlchemy ORM:**
   - Object-relational mapping
   - Relationship management
   - Query optimization
   - Database migrations support

3. **RESTful Design:**
   - Clear endpoint structure
   - Standard HTTP methods
   - JSON request/response
   - CORS enabled

### Frontend

1. **React + TypeScript:**
   - Type safety
   - Component reusability
   - State management with hooks
   - Efficient rendering

2. **Modern UI/UX:**
   - Responsive design
   - Form validation
   - Loading states
   - Error handling

3. **API Integration:**
   - Environment-based configuration
   - Error handling and feedback

### DevOps

1. **Docker Containerization:**
   - Multi-stage builds
   - Service isolation
   - Easy deployment
   - Consistent environments

2. **Docker Compose:**
   - Multi-service orchestration
   - Network configuration
   - Volume management
   - Health checks

3. **Cloudflare Tunnels:**
   - Public access without port forwarding
   - Automatic HTTPS
   - Load balancing
   - DDoS protection

---

## Compliance with Requirements

### Assignment Requirements

✅ **2 Modules Completely Developed:**
   - Student Management Module (fully functional)
   - Grade Management Module (fully functional)

✅ **Class Diagram Matching:**
   - All classes from Experiment 3 implemented
   - All relationships preserved
   - All methods implemented
   - Python OOP follows Java design

✅ **Backend in Python:**
   - FastAPI framework
   - SQLAlchemy ORM
   - Type hints and validation

✅ **Docker Compose Deployment:**
   - Backend service
   - Frontend service
   - Database service
   - Cloudflare tunnels for public access

### Functional Requirements

✅ Student CRUD operations  
✅ Course registration with prerequisite validation  
✅ Grade entry and updates  
✅ CGPA calculation  
✅ Transcript generation  
✅ Backlog detection  
✅ Grade sheet generation  
✅ Data validation and error handling  

---

## Future Enhancements

While the current implementation covers the required 2 modules completely, the system can be extended with:

1. **Additional Modules:**
   - Faculty Management (UC6, UC7)
   - Inventory Management (UC4, UC5)
   - Financial Management (UC10)
   - Report Generation (UC8)

2. **Authentication & Authorization:**
   - JWT-based authentication
   - Role-based access control
   - Session management

3. **Advanced Features:**
   - Email notifications
   - PDF report generation
   - Data export functionality
   - Advanced analytics and dashboards

4. **Performance Optimization:**
   - Caching layer
   - Database indexing
   - Query optimization
   - Load balancing

---

## Conclusion

This project successfully demonstrates a complete full-stack implementation of the University Department Information System based on our UML diagrams and SRS. The system:

- Implements 2 modules completely as required
- Follows the class diagram from Experiment 3 precisely
- Uses Python for backend with FastAPI
- Provides a modern React frontend
- Deploys with Docker Compose
- Includes Cloudflare tunnels for public access

The implementation showcases:
- Object-Oriented Design principles
- RESTful API architecture
- Database design and ORM
- Modern web development practices
- Containerization and deployment
- Alignment with Software Engineering best practices

All use cases are functional, tested, and ready for demonstration.

---

## Team Contributions

**Ruchir Kadam (2023300098):**
- Backend implementation (models, routes, database)
- Docker configuration
- API design and testing

**Amruta Johare (2023300095):**
- Frontend implementation (React components)
- UI/UX design
- Integration testing

---

## References

1. Experiment 2: Use Case Diagrams (SE-Experiment-2.pdf)
2. Experiment 3: Class Diagrams (SE-Experiment-3.pdf)
3. Software Requirements Specification (srs_university-1.pdf)
4. FastAPI Documentation: https://fastapi.tiangolo.com/
5. React Documentation: https://react.dev/
6. SQLAlchemy Documentation: https://docs.sqlalchemy.org/
7. Docker Documentation: https://docs.docker.com/