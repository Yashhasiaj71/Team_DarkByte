import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import UploadPage from './pages/Upload';
import ReportPage from './pages/Report';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/report/:id" element={<ReportPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
