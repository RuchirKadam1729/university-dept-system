import React, { useState, useEffect } from 'react';
import { http } from '../lib/http';

interface Course {
  course_id: string;
  course_name: string;
  credits: number;
  prerequisites: Course[];
}

interface Semester {
  semester_id: string;
  name: string;
  year: number;
}

const CourseManagement: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [semesters, setSemesters] = useState<Semester[]>([]);
  const [loading, setLoading] = useState(true);
  const [newCourse, setNewCourse] = useState({
    course_id: '',
    course_name: '',
    credits: 3,
    prerequisite_ids: [] as string[]
  });
  const [newSemester, setNewSemester] = useState({
    semester_id: '',
    name: '',
    year: new Date().getFullYear()
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [coursesRes, semestersRes] = await Promise.all([
        http.get('/api/courses/'),
        http.get('/api/semesters/')
      ]);
      setCourses(coursesRes.data);
      setSemesters(semestersRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await http.post('/api/courses/', newCourse);
      alert('Course created successfully!');
      setNewCourse({
        course_id: '',
        course_name: '',
        credits: 3,
        prerequisite_ids: []
      });
      fetchData();
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to create course'}`);
    }
  };

  const handleCreateSemester = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await http.post('/api/semesters/', newSemester);
      alert('Semester created successfully!');
      setNewSemester({
        semester_id: '',
        name: '',
        year: new Date().getFullYear()
      });
      fetchData();
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to create semester'}`);
    }
  };

  if (loading) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <h2>Course & Semester Management</h2>

      {/* All Courses */}
      <div className="section">
        <h3>📚 All Available Courses ({courses.length})</h3>
        {courses.length === 0 ? (
          <p className="text-gray-500">No courses available. Create some below!</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {courses.map(course => (
              <div key={course.course_id} className="border rounded-lg p-4 bg-white shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-bold text-lg text-indigo-600">{course.course_id}</h4>
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                    {course.credits} credits
                  </span>
                </div>
                <p className="text-gray-700 mb-2">{course.course_name}</p>
                {course.prerequisites && course.prerequisites.length > 0 && (
                  <div className="text-sm text-gray-600">
                    <strong>Prerequisites:</strong>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {course.prerequisites.map(prereq => (
                        <span key={prereq.course_id} className="px-2 py-0.5 bg-gray-200 rounded">
                          {prereq.course_id}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* All Semesters */}
      <div className="section">
        <h3>📅 All Semesters ({semesters.length})</h3>
        {semesters.length === 0 ? (
          <p className="text-gray-500">No semesters available. Create some below!</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {semesters.map(semester => (
              <div key={semester.semester_id} className="border rounded-lg p-3 bg-white shadow-sm">
                <h4 className="font-bold text-indigo-600">{semester.semester_id}</h4>
                <p className="text-gray-700 text-sm">{semester.name}</p>
                <p className="text-gray-500 text-xs">Year: {semester.year}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Reference for Course Registration */}
      <div className="section bg-blue-50 border-l-4 border-blue-400 p-4">
        <h3 className="text-blue-800 mb-2">💡 Quick Reference for Course Registration</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-semibold text-blue-700 mb-2">Sample Course IDs:</h4>
            <div className="text-sm space-y-1">
              {courses.slice(0, 8).map(c => (
                <div key={c.course_id} className="flex justify-between">
                  <span className="font-mono font-semibold">{c.course_id}</span>
                  <span className="text-gray-600">{c.credits} cr</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-blue-700 mb-2">Sample Semester IDs:</h4>
            <div className="text-sm space-y-1">
              {semesters.slice(0, 4).map(s => (
                <div key={s.semester_id}>
                  <span className="font-mono font-semibold">{s.semester_id}</span>
                  <span className="text-gray-600 ml-2">({s.name})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Create Course Form */}
      <div className="section">
        <h3>➕ Create New Course</h3>
        <form onSubmit={handleCreateCourse} className="form">
          <input
            type="text"
            placeholder="Course ID (e.g., CS101)"
            value={newCourse.course_id}
            onChange={(e) => setNewCourse({...newCourse, course_id: e.target.value.toUpperCase()})}
            required
          />
          <input
            type="text"
            placeholder="Course Name"
            value={newCourse.course_name}
            onChange={(e) => setNewCourse({...newCourse, course_name: e.target.value})}
            required
          />
          <input
            type="number"
            placeholder="Credits"
            min="1"
            max="6"
            value={newCourse.credits}
            onChange={(e) => setNewCourse({...newCourse, credits: parseInt(e.target.value)})}
            required
          />
          <input
            type="text"
            placeholder="Prerequisite IDs (comma-separated, e.g., CS101,MATH101)"
            value={newCourse.prerequisite_ids.join(',')}
            onChange={(e) => setNewCourse({
              ...newCourse, 
              prerequisite_ids: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
            })}
          />
          <button type="submit" className="btn-primary">Create Course</button>
        </form>
      </div>

      {/* Create Semester Form */}
      <div className="section">
        <h3>➕ Create New Semester</h3>
        <form onSubmit={handleCreateSemester} className="form">
          <input
            type="text"
            placeholder="Semester ID (e.g., FALL2024)"
            value={newSemester.semester_id}
            onChange={(e) => setNewSemester({...newSemester, semester_id: e.target.value.toUpperCase()})}
            required
          />
          <input
            type="text"
            placeholder="Name (e.g., Fall 2024)"
            value={newSemester.name}
            onChange={(e) => setNewSemester({...newSemester, name: e.target.value})}
            required
          />
          <input
            type="number"
            placeholder="Year"
            min="2020"
            max="2030"
            value={newSemester.year}
            onChange={(e) => setNewSemester({...newSemester, year: parseInt(e.target.value)})}
            required
          />
          <button type="submit" className="btn-primary">Create Semester</button>
        </form>
      </div>
    </div>
  );
};

export default CourseManagement;