import pytest

@pytest.mark.asyncio
async def test_enter_grade_success(client, sample_student, sample_course, sample_semester):
    """Test UC2: Enter Grades - successful grade entry"""
    # First register student for course
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    # Enter grade
    payload = {
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A",
        "semester_id": "SEM1"
    }
    response = client.post("/grades/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["grade_value"] == "A"
    assert data["course_id"] == "CS101"

@pytest.mark.asyncio
async def test_enter_grade_updates_cgpa(client, sample_student, sample_course, sample_semester):
    """Test that entering grades updates student CGPA"""
    # Register and enter grade
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A",
        "semester_id": "SEM1"
    })
    
    # Check student CGPA updated
    response = client.get("/students/2023001/")
    assert response.status_code == 200
    data = response.json()
    assert data["cgpa"] > 0.0  # CGPA should be calculated

@pytest.mark.asyncio
async def test_update_existing_grade(client, sample_student, sample_course, sample_semester):
    """Test updating an existing grade"""
    # Register and enter initial grade
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "B",
        "semester_id": "SEM1"
    })
    
    # Update grade
    response = client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A+",
        "semester_id": "SEM1"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["grade_value"] == "A+"

@pytest.mark.asyncio
async def test_invalid_grade_value(client, sample_student, sample_course, sample_semester):
    """Test that invalid grade values are rejected"""
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    payload = {
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "X",  # Invalid grade
        "semester_id": "SEM1"
    }
    response = client.post("/grades/", json=payload)
    
    assert response.status_code in [400, 422]  # Should reject invalid grade

@pytest.mark.asyncio
async def test_get_grades_by_student(client, sample_student, sample_course, sample_semester):
    """Test UC3: Get Grades - retrieve grades by student"""
    # Setup: Register and enter grade
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A",
        "semester_id": "SEM1"
    })
    
    # Get grades
    response = client.get("/grades/student/2023001/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["student_roll_number"] == "2023001"

@pytest.mark.asyncio
async def test_get_grades_by_course(client, sample_student, sample_course, sample_semester):
    """Test retrieving grades by course"""
    # Setup
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A",
        "semester_id": "SEM1"
    })
    
    # Get grades by course
    response = client.get("/grades/course/CS101/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_filter_grades_by_semester(client, sample_student, sample_course, sample_semester):
    """Test filtering grades by semester"""
    # Setup
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A",
        "semester_id": "SEM1"
    })
    
    # Get grades with semester filter
    response = client.get("/grades/student/2023001/?semester_id=SEM1")
    
    assert response.status_code == 200
    data = response.json()
    assert all(g["semester_id"] == "SEM1" for g in data)

@pytest.mark.asyncio
async def test_generate_gradesheet(client, sample_student, sample_course, sample_semester):
    """Test generating grade sheet with GPA calculation"""
    # Setup
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A",
        "semester_id": "SEM1"
    })
    
    # Generate grade sheet
    payload = {
        "student_roll_number": "2023001",
        "semester_id": "SEM1"
    }
    response = client.post("/grades/gradesheet/generate/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "gpa" in data
    assert data["gpa"] > 0.0

@pytest.mark.asyncio
async def test_get_gradesheets(client, sample_student):
    """Test retrieving all grade sheets for a student"""
    response = client.get("/grades/gradesheet/2023001/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_failing_grade_creates_backlog(client, sample_student, sample_course, sample_semester):
    """Test that F grade creates a backlog"""
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    # Enter failing grade
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "F",
        "semester_id": "SEM1"
    })
    
    # Check backlogs
    response = client.get("/students/2023001/backlogs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(b["course_id"] == "CS101" for b in data)