import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Upload, FileText, User } from 'lucide-react';
import './Sidebar.css';

const Sidebar = () => {
    const location = useLocation();

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2>Plagiarism Detection</h2>
            </div>
            <nav className="sidebar-nav">
                <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
                    <Home size={20} /> Dashboard
                </Link>
                <Link to="/upload" className={location.pathname === '/upload' ? 'active' : ''}>
                    <Upload size={20} /> Upload Assignment
                </Link>
                {/* <Link to="/students">
                    <User size={20} /> Students
                </Link> */}
            </nav>
        </div>
    );
};

export default Sidebar;
