import React, { useState, useEffect } from 'react';
import { http } from '../lib/http';

interface Student {
  roll_number: string;
  name: string;
  address: string;
  admission_date: string;
  cgpa: number;
}

interface Registration {
  course_id: string;
  semester_id: string;
}

const StudentManagement: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [newStudent, setNewStudent] = useState({
    roll_number: '',
    name: '',
    address: '',
    admission_date: new Date().toISOString().split('T')[0]
  });
  const [selectedStudent, setSelectedStudent] = useState<string>('');
  const [transcript, setTranscript] = useState<any>(null);
  const [registration, setRegistration] = useState<Registration>({
    course_id: '',
    semester_id: ''
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await http.get('/api/students/');
      setStudents(response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  const handleCreateStudent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await http.post('/api/students/', newStudent);
      alert('Student registered successfully!');
      setNewStudent({
        roll_number: '',
        name: '',
        address: '',
        admission_date: new Date().toISOString().split('T')[0]
      });
      fetchStudents();
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to register student'}`);
    }
  };

  const handleViewTranscript = async () => {
    if (!selectedStudent) {
      alert('Please select a student');
      return;
    }
    try {
      const response = await http.get(`/api/students/${selectedStudent}/transcript/`);
      setTranscript(response.data);
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to fetch transcript'}`);
    }
  };

  const handleRegisterCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStudent) {
      alert('Please select a student');
      return;
    }
    try {
      await http.post(`/api/students/${selectedStudent}/register-course/`, {
        student_roll_number: selectedStudent,
        ...registration
      });
      alert('Course registered successfully!');
      setRegistration({ course_id: '', semester_id: '' });
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to register course'}`);
    }
  };

  return (
    <div className="container">
      <h2>Student Management Module</h2>
      
      <div className="section">
        <h3>Register New Student (UC1)</h3>
        <form onSubmit={handleCreateStudent} className="form">
          <input
            type="text"
            placeholder="Roll Number"
            value={newStudent.roll_number}
            onChange={(e) => setNewStudent({...newStudent, roll_number: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Name"
            value={newStudent.name}
            onChange={(e) => setNewStudent({...newStudent, name: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Address"
            value={newStudent.address}
            onChange={(e) => setNewStudent({...newStudent, address: e.target.value})}
          />
          <input
            type="date"
            value={newStudent.admission_date}
            onChange={(e) => setNewStudent({...newStudent, admission_date: e.target.value})}
            required
          />
          <button type="submit" className="btn-primary">Register Student</button>
        </form>
      </div>

      <div className="section">
        <h3>All Students (UC9 - Get Student Data)</h3>
        <div className="student-list">
          {students.map(student => (
            <div key={student.roll_number} className="student-card">
              <strong>{student.name}</strong> ({student.roll_number})
              <br />CGPA: {student.cgpa.toFixed(2)}
              <button 
                onClick={() => setSelectedStudent(student.roll_number)}
                className="btn-small"
              >
                Select
              </button>
            </div>
          ))}
        </div>
      </div>

      {selectedStudent && (
        <>
          <div className="section">
            <h3>Register Course for {selectedStudent}</h3>
            <form onSubmit={handleRegisterCourse} className="form">
              <input
                type="text"
                placeholder="Course ID"
                value={registration.course_id}
                onChange={(e) => setRegistration({...registration, course_id: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Semester ID"
                value={registration.semester_id}
                onChange={(e) => setRegistration({...registration, semester_id: e.target.value})}
                required
              />
              <button type="submit" className="btn-primary">Register Course</button>
            </form>
          </div>

          <div className="section">
            <h3>View Transcript</h3>
            <button onClick={handleViewTranscript} className="btn-primary">
              Load Transcript for {selectedStudent}
            </button>
            
            {transcript && (
              <div className="transcript">
                <h4>Student: {transcript.student.name}</h4>
                <p>Roll Number: {transcript.student.roll_number}</p>
                <p><strong>CGPA: {transcript.cgpa.toFixed(2)}</strong></p>
                
                <h5>Grades:</h5>
                {transcript.grades.length > 0 ? (
                  <table>
                    <thead>
                      <tr>
                        <th>Course</th>
                        <th>Grade</th>
                        <th>Semester</th>
                      </tr>
                    </thead>
                    <tbody>
                      {transcript.grades.map((grade: any) => (
                        <tr key={grade.grade_id}>
                          <td>{grade.course_id}</td>
                          <td>{grade.grade_value}</td>
                          <td>{grade.semester_id}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p>No grades available</p>
                )}

                <h5>Backlogs:</h5>
                {transcript.backlogs.length > 0 ? (
                  <ul>
                    {transcript.backlogs.map((backlog: any) => (
                      <li key={backlog.registration_id}>
                        {backlog.course_id} - {backlog.semester_id}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No backlogs</p>
                )}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default StudentManagement;