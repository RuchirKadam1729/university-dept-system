import pytest

@pytest.mark.asyncio
async def test_create_course_success(client):
    """Test creating a new course"""
    payload = {
        "course_id": "CS999",
        "course_name": "Test Course",
        "credits": 3,
        "prerequisite_ids": []
    }
    response = client.post("/courses/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == "CS999"
    assert data["course_name"] == "Test Course"
    assert data["credits"] == 3

@pytest.mark.asyncio
async def test_create_course_with_prerequisites(client, sample_course):
    """Test creating course with prerequisites"""
    payload = {
        "course_id": "CS202",
        "course_name": "Advanced Course",
        "credits": 4,
        "prerequisite_ids": ["CS101"]
    }
    response = client.post("/courses/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == "CS202"

@pytest.mark.asyncio
async def test_get_all_courses(client, sample_course):
    """Test listing all courses"""
    response = client.get("/courses/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_course_by_id(client, sample_course):
    """Test getting specific course"""
    response = client.get("/courses/CS101/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == "CS101"

@pytest.mark.asyncio
async def test_prerequisite_validation_success(client, sample_course, sample_course_with_prereq, sample_student, sample_semester):
    """Test prerequisite validation works correctly"""
    # Complete prerequisite first
    client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    })
    
    # Enter passing grade
    client.post("/grades/", json={
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "grade_value": "A",
        "semester_id": "SEM1"
    })
    
    # Now should be able to register for CS201
    response = client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS201",
        "semester_id": "SEM1"
    })
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_prerequisite_validation_failure(client, sample_course_with_prereq, sample_student, sample_semester):
    """Test prerequisite validation prevents registration"""
    # Try to register without completing CS101
    response = client.post("/students/2023001/register-course/", json={
        "student_roll_number": "2023001",
        "course_id": "CS201",
        "semester_id": "SEM1"
    })
    
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_semester(client):
    """Test creating a semester"""
    payload = {
        "semester_id": "SEM2",
        "name": "Spring 2025",
        "year": 2025
    }
    response = client.post("/semesters/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["semester_id"] == "SEM2"

@pytest.mark.asyncio
async def test_get_all_semesters(client, sample_semester):
    """Test listing all semesters"""
    response = client.get("/semesters/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0