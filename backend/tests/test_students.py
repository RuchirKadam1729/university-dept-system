import pytest

@pytest.mark.asyncio
async def test_register_student_success(client):
    """Test UC1: Register Student - successful registration"""
    payload = {
        "roll_number": "2023001",
        "name": "John Doe",
        "address": "123 Main Street",
        "admission_date": "2023-08-01"
    }
    response = client.post("/students/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["roll_number"] == payload["roll_number"]
    assert data["name"] == payload["name"]
    assert data["cgpa"] == 0.0  # Initial CGPA should be 0

@pytest.mark.asyncio
async def test_register_duplicate_student_fails(client, sample_student):
    """Test duplicate student registration is prevented"""
    payload = {
        "roll_number": "2023001",  # Same as sample_student
        "name": "Jane Doe",
        "address": "456 Other St",
        "admission_date": "2023-08-01"
    }
    response = client.post("/students/", json=payload)
    
    assert response.status_code == 400  # Should fail with duplicate

@pytest.mark.asyncio
async def test_get_all_students(client, sample_student):
    """Test UC9: Get Student Data - list all students"""
    response = client.get("/students/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(s["roll_number"] == "2023001" for s in data)

@pytest.mark.asyncio
async def test_get_student_by_roll_number(client, sample_student):
    """Test UC9: Get Student Data - get specific student"""
    response = client.get("/students/2023001/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["roll_number"] == "2023001"
    assert data["name"] == "John Doe"

@pytest.mark.asyncio
async def test_get_nonexistent_student(client):
    """Test getting student that doesn't exist"""
    response = client.get("/students/9999999/")
    
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_student_info(client, sample_student):
    """Test updating student information"""
    payload = {
        "name": "John Updated",
        "address": "999 New Address",
        "admission_date": "2023-08-01"
    }
    response = client.put("/students/2023001/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Updated"
    assert data["address"] == "999 New Address"

@pytest.mark.asyncio
async def test_register_course_success(client, sample_student, sample_course, sample_semester):
    """Test course registration - successful registration"""
    payload = {
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    }
    response = client.post("/students/2023001/register-course/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == "CS101"
    assert data["student_roll_number"] == "2023001"

@pytest.mark.asyncio
async def test_register_course_duplicate_prevented(client, sample_student, sample_course, sample_semester):
    """Test duplicate course registration is prevented"""
    payload = {
        "student_roll_number": "2023001",
        "course_id": "CS101",
        "semester_id": "SEM1"
    }
    # Register once
    client.post("/students/2023001/register-course/", json=payload)
    
    # Try to register again
    response = client.post("/students/2023001/register-course/", json=payload)
    
    assert response.status_code == 400  # Should prevent duplicate

@pytest.mark.asyncio
async def test_register_course_prerequisite_check(client, sample_student, sample_course_with_prereq, sample_semester):
    """Test prerequisite validation during course registration"""
    payload = {
        "student_roll_number": "2023001",
        "course_id": "CS201",  # Has CS101 as prerequisite
        "semester_id": "SEM1"
    }
    response = client.post("/students/2023001/register-course/", json=payload)
    
    # Should fail because CS101 not completed
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_student_transcript(client, sample_student):
    """Test viewing student transcript"""
    response = client.get("/students/2023001/transcript/")
    
    assert response.status_code == 200
    data = response.json()
    assert "student" in data
    assert "grades" in data
    assert data["student"]["roll_number"] == "2023001"

@pytest.mark.asyncio
async def test_get_student_backlogs(client, sample_student):
    """Test getting student backlogs"""
    response = client.get("/students/2023001/backlogs/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)