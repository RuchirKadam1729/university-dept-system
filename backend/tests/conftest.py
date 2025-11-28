import os
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.database import Base, get_db
from app.main import app

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override database dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test Client Fixture
@pytest.fixture(scope="function")
def client():
    """Provides a TestClient instance for making API requests."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as tc:
        yield tc
    Base.metadata.drop_all(bind=engine)

# Sample data fixtures
@pytest.fixture
def sample_semester(client):
    """Creates a sample semester for testing."""
    response = client.post("/semesters/", json={
        "semester_id": "SEM1",
        "name": "Fall 2024",
        "year": 2024
    })
    return response.json()

@pytest.fixture
def sample_course(client):
    """Creates a sample course for testing."""
    response = client.post("/courses/", json={
        "course_id": "CS101",
        "course_name": "Introduction to Programming",
        "credits": 4,
        "prerequisite_ids": []
    })
    return response.json()

@pytest.fixture
def sample_course_with_prereq(client, sample_course):
    """Creates a course with prerequisites."""
    response = client.post("/courses/", json={
        "course_id": "CS201",
        "course_name": "Data Structures",
        "credits": 4,
        "prerequisite_ids": ["CS101"]
    })
    return response.json()

@pytest.fixture
def sample_student(client):
    """Creates a sample student for testing."""
    response = client.post("/students/", json={
        "roll_number": "2023001",
        "name": "John Doe",
        "address": "123 Main St",
        "admission_date": "2023-08-01"
    })
    return response.json()

# Test Results Logger
LOG_FILE = "tests/test_results.txt"

def pytest_sessionstart(session):
    """Called before test run starts"""
    with open(LOG_FILE, "w") as f:
        f.write("=" * 70 + "\n")
        f.write(f"UNIVERSITY DEPARTMENT SYSTEM - UNIT TEST RUN\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

def pytest_runtest_logreport(report):
    """Called after each test phase"""
    if report.when == "call":
        with open(LOG_FILE, "a") as f:
            status = "✅ PASSED" if report.passed else "❌ FAILED"
            test_name = report.nodeid.split("::")[-1]
            f.write(f"{status} | {test_name}\n")
            if report.failed:
                reason = report.longreprtext.split('AssertionError:')[-1].strip() if 'AssertionError' in report.longreprtext else 'See details'
                f.write(f"  └─ Reason: {reason}\n")
            f.write("\n")

def pytest_sessionfinish(session, exitstatus):
    """Called after test run finishes"""
    with open(LOG_FILE, "a") as f:
        f.write("=" * 70 + "\n")
        f.write(f"RESULT: {'ALL TESTS PASSED ✅' if exitstatus == 0 else 'SOME TESTS FAILED ❌'}\n")
        f.write(f"Exit Code: {exitstatus}\n")
        f.write("=" * 70 + "\n")