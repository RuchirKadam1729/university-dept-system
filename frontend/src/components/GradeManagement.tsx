import React, { useState } from 'react';
import { http } from '../lib/http';

interface Grade {
  grade_id: number;
  student_roll_number: string;
  course_id: string;
  grade_value: string;
  semester_id: string;
}

const GradeManagement: React.FC = () => {
  const [gradeEntry, setGradeEntry] = useState({
    student_roll_number: '',
    course_id: '',
    grade_value: '',
    semester_id: ''
  });
  const [queryRoll, setQueryRoll] = useState('');
  const [querySemester, setQuerySemester] = useState('');
  const [grades, setGrades] = useState<Grade[]>([]);
  const [gradeSheet, setGradeSheet] = useState<any>(null);

  const handleEnterGrade = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await http.post('/api/grades/', gradeEntry);
      alert('Grade entered successfully!');
      setGradeEntry({
        student_roll_number: '',
        course_id: '',
        grade_value: '',
        semester_id: ''
      });
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to enter grade'}`);
    }
  };

  const handleGetGrades = async () => {
    if (!queryRoll) {
      alert('Please enter student roll number');
      return;
    }
    try {
      const url = querySemester 
        ? `/api/grades/student/${queryRoll}/?semester_id=${querySemester}`
        : `/api/grades/student/${queryRoll}/`;
      const response = await http.get(url);
      setGrades(response.data);
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to fetch grades'}`);
    }
  };

  const handleGenerateGradeSheet = async () => {
    if (!queryRoll || !querySemester) {
      alert('Please enter both student roll number and semester ID');
      return;
    }
    try {
      // FIXED: Send as JSON body, not query params
      const response = await http.post('/api/grades/gradesheet/generate/', {
        student_roll_number: queryRoll,
        semester_id: querySemester
      });
      setGradeSheet(response.data);
      alert(`Grade Sheet Generated! GPA: ${response.data.gpa}`);
    } catch (error: any) {
      const message = error?.response?.data?.detail || error.message || 'Failed to generate grade sheet';
      alert(`Error: ${message}`);
    }
  };

  return (
    <div className="container">
      <h2>Grade Management Module</h2>
      
      <div className="section">
        <h3>Enter Grade (UC2 - Enter Grades)</h3>
        <form onSubmit={handleEnterGrade} className="form">
          <input
            type="text"
            placeholder="Student Roll Number"
            value={gradeEntry.student_roll_number}
            onChange={(e) => setGradeEntry({...gradeEntry, student_roll_number: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Course ID"
            value={gradeEntry.course_id}
            onChange={(e) => setGradeEntry({...gradeEntry, course_id: e.target.value})}
            required
          />
          <select
            value={gradeEntry.grade_value}
            onChange={(e) => setGradeEntry({...gradeEntry, grade_value: e.target.value})}
            required
          >
            <option value="">Select Grade</option>
            <option value="A+">A+</option>
            <option value="A">A</option>
            <option value="B+">B+</option>
            <option value="B">B</option>
            <option value="C+">C+</option>
            <option value="C">C</option>
            <option value="D">D</option>
            <option value="F">F</option>
          </select>
          <input
            type="text"
            placeholder="Semester ID"
            value={gradeEntry.semester_id}
            onChange={(e) => setGradeEntry({...gradeEntry, semester_id: e.target.value})}
            required
          />
          <button type="submit" className="btn-primary">Enter Grade</button>
        </form>
      </div>

      <div className="section">
        <h3>Get Grades (UC3 - Get Grades)</h3>
        <div className="form">
          <input
            type="text"
            placeholder="Student Roll Number"
            value={queryRoll}
            onChange={(e) => setQueryRoll(e.target.value)}
          />
          <input
            type="text"
            placeholder="Semester ID (optional)"
            value={querySemester}
            onChange={(e) => setQuerySemester(e.target.value)}
          />
          <button onClick={handleGetGrades} className="btn-primary">
            Get Grades
          </button>
        </div>

        {grades.length > 0 && (
          <div className="grades-list">
            <h4>Grades for {queryRoll}</h4>
            <table>
              <thead>
                <tr>
                  <th>Course ID</th>
                  <th>Grade</th>
                  <th>Semester</th>
                </tr>
              </thead>
              <tbody>
                {grades.map(grade => (
                  <tr key={grade.grade_id}>
                    <td>{grade.course_id}</td>
                    <td><strong>{grade.grade_value}</strong></td>
                    <td>{grade.semester_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="section">
        <h3>Generate Grade Sheet</h3>
        <div className="form">
          <input
            type="text"
            placeholder="Student Roll Number"
            value={queryRoll}
            onChange={(e) => setQueryRoll(e.target.value)}
          />
          <input
            type="text"
            placeholder="Semester ID"
            value={querySemester}
            onChange={(e) => setQuerySemester(e.target.value)}
          />
          <button onClick={handleGenerateGradeSheet} className="btn-primary">
            Generate Grade Sheet
          </button>
        </div>

        {gradeSheet && (
          <div className="grade-sheet">
            <h4>Grade Sheet</h4>
            <p>Student: {gradeSheet.student_roll_number}</p>
            <p>Semester: {gradeSheet.semester_id}</p>
            <p><strong>GPA: {gradeSheet.gpa.toFixed(2)}</strong></p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GradeManagement;