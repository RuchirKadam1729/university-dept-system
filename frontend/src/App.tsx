import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import StudentManagement from './components/StudentManagement';
import GradeManagement from './components/GradeManagement';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">University Department System</h1>
            <div className="nav-links">
              <Link to="/" className="nav-link">Students</Link>
              <Link to="/grades" className="nav-link">Grades</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<StudentManagement />} />
            <Route path="/grades" element={<GradeManagement />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;